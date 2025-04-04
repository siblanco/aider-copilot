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
        with GitTemporaryDirectory():
            # Setup IO and Coder
            io = InputOutput(pretty=False, yes=True) # Use yes=True for auto-apply
            coder = Coder.create(self.GPT35, "diff", io=io)
            commands = Commands(io, coder)

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
            # 2. End condition check response (NO first, then YES)
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

            # --- Simulate first iteration ---
            coder.run_loop_iteration()

            # Assertions for first iteration
            mock_send_message.assert_called_with("Refactor this code")
            mock_apply_updates.assert_called_with()  # Called after send_message
            mock_run_cmd.assert_called_with(
                "python check_script.py", verbose=False, error_print=io.tool_error, cwd=coder.root
            )
            mock_simple_send.assert_called_with(
                [{"role": "user", "content": mock.ANY}]  # Check end condition prompt
            )
            self.assertIn("Output without SUCCESS", mock_simple_send.call_args[0][0][0]["content"])
            self.assertIn(
                "Does the output contain 'SUCCESS'?",
                mock_simple_send.call_args[0][0][0]["content"],
            )
            self.assertTrue(coder.loop_running) # Loop should continue
            self.assertEqual(coder.loop_iteration, 1)

            # --- Simulate second iteration ---
            coder.run_loop_iteration()

            # Assertions for second iteration
            self.assertEqual(mock_send_message.call_count, 2)
            self.assertEqual(mock_apply_updates.call_count, 2)
            self.assertEqual(mock_run_cmd.call_count, 2)
            self.assertEqual(mock_simple_send.call_count, 2)
            self.assertIn("Output with SUCCESS", mock_simple_send.call_args[0][0][0]["content"])
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

            # Mock Coder.create and its run method to prevent actual execution
            with patch("aider.main.Coder.create") as mock_coder_create:
                mock_coder_instance = MagicMock()
                mock_coder_instance.loop_running = False  # Start as not running
                # Create Commands *inside* the patch context using the mock coder
                mock_coder_instance.commands = Commands(io, mock_coder_instance)
                # Mock start_loop to check if it's called
                mock_coder_instance.start_loop = MagicMock()
                mock_coder_create.return_value = mock_coder_instance

                # Call main with --loop argument
                from aider.main import main

                main(["--loop", "--exit"])  # --exit prevents entering the main loop

                # Assert prompt_ask was called 4 times for configuration
                self.assertEqual(io.prompt_ask.call_count, 4)
                # Assert start_loop was called on the coder instance
                mock_coder_instance.start_loop.assert_called_once_with(
                    "Initial Task", "initial command", "initial end condition", True # auto_clear=True
                )


if __name__ == "__main__":
    unittest.main()
