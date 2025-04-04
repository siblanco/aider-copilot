import os
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock, patch

from aider.coders import Coder
from aider.commands import Commands
from aider.io import InputOutput
from aider.models import Model
from aider.utils import GitTemporaryDirectory


class TestLoopMode(unittest.TestCase):
    def setUp(self):
        self.GPT35 = Model("gpt-3.5-turbo")

    @patch("aider.coders.base_coder.Coder.send_message")
    @patch("aider.coders.base_coder.Coder.apply_updates")
    @patch("aider.coders.base_coder.run_cmd")
    @patch("aider.models.Model.simple_send_with_retries")
    def test_loop_mode_basic_flow(
        self,
        mock_simple_send,
        mock_run_cmd,
        mock_apply_updates,
        mock_send_message,
    ):
        with GitTemporaryDirectory() as temp_dir:
            # Setup IO and Coder
            io = InputOutput(pretty=False, yes=True) # Use yes=True for auto-apply
            coder = Coder.create(self.GPT35, "diff", io=io)
            # Explicitly enable auto-commit for the test
            coder.auto_commit_after_apply = True
            commands = Commands(io, coder)

            # Create and commit file1.py so auto_commit works
            file1_path = Path(temp_dir) / "file1.py"
            file1_path.write_text("initial content")
            # Use filename directly for adding to git index
            coder.repo.repo.index.add([file1_path.name])
            coder.repo.repo.index.commit("add file1.py")

            # Mock user inputs for loop configuration
            io.prompt_ask = MagicMock(
                side_effect=[
                    "Refactor this code",             # Task
                    "python check_script.py",         # Command
                    "Does the output contain 'SUCCESS'?", # End condition
                    "yes",                            # Auto-clear
                ]
            )

            # Mock LLM responses
            # 1. Initial task response (suggests edits)
            mock_send_message.return_value = iter([]) # Simulate no streaming output needed for test
            # 2. End condition check response (NO first, then YES) - Commit messages are mocked away
            mock_simple_send.side_effect = ["NO", "YES"]

            # Mock apply_updates to return edited files
            mock_apply_updates.return_value = {"file1.py"}

            # Mock run_cmd output
            mock_run_cmd.side_effect = [
                (0, "Output without SUCCESS"), # First iteration
                (0, "Output with SUCCESS"),   # Second iteration
            ]

            # Start the loop configuration via command
            commands.cmd_loop("")

            # Assert loop state is configured
            self.assertTrue(coder.loop_running)
            self.assertEqual(coder.loop_task, "Refactor this code")
            self.assertEqual(coder.loop_command, "python check_script.py")
            self.assertEqual(coder.loop_end_condition, "Does the output contain 'SUCCESS'?")
            self.assertTrue(coder.loop_auto_clear) # Check auto-clear setting
            self.assertTrue(coder.berserk_mode) # Loop enables berserk

            # Patch coder.auto_commit for the iterations
            with patch.object(coder, 'auto_commit', return_value=("dummy_hash", "dummy commit message")) as mock_auto_commit:
                # --- Simulate first iteration ---
                coder.run_loop_iteration()

                # Assertions for first iteration
                mock_send_message.assert_called_with("Refactor this code")
                mock_apply_updates.assert_called_with()  # Called after send_message
            mock_run_cmd.assert_called_with(
                "python check_script.py", verbose=False, error_print=io.tool_error, cwd=coder.root
            )
            # Assertions for first iteration's end condition check
            # simple_send is only called for end condition check now (call 0)
            mock_auto_commit.assert_called_once_with({'file1.py'}) # Check that auto_commit was called with edited files
            mock_simple_send.assert_called_once() # Only end condition check
            end_condition_call_args = mock_simple_send.call_args_list[0][0][0] # Args of the first call
            self.assertEqual(end_condition_call_args[0]["role"], "user")
            self.assertIn("Output without SUCCESS", end_condition_call_args[0]["content"])
            self.assertIn("Does the output contain 'SUCCESS'?", end_condition_call_args[0]["content"])
            self.assertTrue(coder.loop_running) # Loop should continue
            self.assertEqual(coder.loop_iteration, 1)

            # --- Simulate second iteration ---
                # Reset mocks for the second iteration's commit and end condition check
                mock_auto_commit.reset_mock()
                mock_simple_send.reset_mock()
                coder.run_loop_iteration()

                # Assertions for second iteration
                self.assertEqual(mock_send_message.call_count, 2)  # Task sent twice
                self.assertEqual(mock_apply_updates.call_count, 2) # Updates applied twice
                self.assertEqual(mock_run_cmd.call_count, 2)       # Command run twice
                self.assertEqual(mock_auto_commit.call_count, 1)   # Auto-commit called once in 2nd iter
                self.assertEqual(mock_simple_send.call_count, 1)   # End check called once in 2nd iter

                # Check the second end condition call (1st call in 2nd iter)
                end_condition_call_args_2 = mock_simple_send.call_args_list[0][0][0]
                self.assertIn("Output with SUCCESS", end_condition_call_args_2[0]["content"])
                self.assertFalse(coder.loop_running)  # Loop should stop
                self.assertEqual(coder.loop_iteration, 2)

    @patch("aider.coders.base_coder.Coder.send_message")
    @patch("aider.coders.base_coder.Coder.apply_updates")
    @patch("aider.coders.base_coder.run_cmd")
    def test_exitloop_command(
        self, mock_run_cmd, mock_apply_updates, mock_send_message
    ):
        with GitTemporaryDirectory():
            io = InputOutput(pretty=False, yes=True)
            coder = Coder.create(self.GPT35, "diff", io=io)
            commands = Commands(io, coder)

            # Configure loop manually for testing /exitloop
            coder.loop_task = "task"
            coder.loop_command = "cmd"
            coder.loop_end_condition = "end"
            coder.loop_running = True
            coder.berserk_mode = True
            io.berserk_mode = True

            self.assertTrue(coder.loop_running)
            self.assertTrue(coder.berserk_mode)

            # Run /exitloop
            commands.cmd_exitloop("")

            # Assert loop is stopped
            self.assertFalse(coder.loop_running)
            # Assert berserk mode is potentially restored (though stop_loop doesn't do this yet)
            # self.assertFalse(coder.berserk_mode)

    def test_loop_argument_starts_configuration(self):
         with GitTemporaryDirectory():
            io = InputOutput(pretty=False, yes=True)
            # Mock user inputs for loop configuration during main() call
            io.prompt_ask = MagicMock(
                side_effect=[
                    "Initial Task",
                    "initial command",
                    "initial end condition",
                    "yes", # Auto-clear
                ]
            )

            # Mock Coder.create and Commands within aider.main
            with patch("aider.main.Coder.create") as mock_coder_create, \
                 patch("aider.main.Commands") as mock_commands_class:

                mock_coder_instance = MagicMock()
                mock_coder_instance.loop_running = False  # Start as not running
                mock_coder_instance.start_loop = MagicMock()
                mock_coder_create.return_value = mock_coder_instance

                # Configure the mock Commands instance that main will create
                mock_commands_instance = MagicMock()
                # Link the mock coder to the mock commands instance
                mock_commands_instance.coder = mock_coder_instance
                # Make cmd_loop available on the mock commands instance
                # We need the *real* cmd_loop logic for the test prompts
                real_commands = Commands(io, mock_coder_instance)
                mock_commands_instance.cmd_loop = real_commands.cmd_loop
                mock_commands_class.return_value = mock_commands_instance


                # Call main with --loop argument
                from aider.main import main

                main(["--loop", "--exit"])  # --exit prevents entering the main loop

                # Assert prompt_ask was called 4 times for configuration
                self.assertEqual(io.prompt_ask.call_count, 4)
                # Assert start_loop was called on the *mock coder instance*
                # (which was linked to the mock commands instance)
                mock_coder_instance.start_loop.assert_called_once_with(
                    "Initial Task", "initial command", "initial end condition", True # auto_clear=True
                )


if __name__ == "__main__":
    unittest.main()
