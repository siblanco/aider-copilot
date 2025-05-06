
<!-- Edit README.md, not index.md -->

# Aider is AI pair programming in your terminal

Aider lets you pair program with LLMs,
to edit code in your local git repository.
Start a new project or work with an existing code base.
Aider works best with Claude 3.7 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o. Aider can [connect to almost any LLM, including local models](https://aider.chat/docs/llms.html).

<!-- SCREENCAST START -->
<p align="center">
  <img
    src="https://aider.chat/assets/screencast.svg"
    alt="aider screencast"
  >
</p>
<!-- SCREENCAST END -->

<!-- VIDEO START
<p align="center">
  <video style="max-width: 100%; height: auto;" autoplay loop muted playsinline>
    <source src="/assets/shell-cmds-small.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>
VIDEO END -->

<p align="center">
<!--[[[cog
from scripts.homepage import get_badges_md
text = get_badges_md()
cog.out(text)
]]]-->
  <a href="https://github.com/Aider-AI/aider/stargazers"><img alt="GitHub Stars" title="Total number of GitHub stars the Aider project has received"
src="https://img.shields.io/github/stars/Aider-AI/aider?style=flat-square&logo=github&color=f1c40f&labelColor=555555"/></a>
  <a href="https://pypi.org/project/aider-chat/"><img alt="PyPI Downloads" title="Total number of installations via pip from PyPI"
src="https://img.shields.io/badge/📦%20Installs-2.1M-2ecc71?style=flat-square&labelColor=555555"/></a>
  <img alt="Tokens per week" title="Number of tokens processed weekly by Aider users"
src="https://img.shields.io/badge/📈%20Tokens%2Fweek-15B-3498db?style=flat-square&labelColor=555555"/>
  <a href="https://openrouter.ai/#options-menu"><img alt="OpenRouter Ranking" title="Aider's ranking among applications on the OpenRouter platform"
src="https://img.shields.io/badge/🏆%20OpenRouter-Top%2020-9b59b6?style=flat-square&labelColor=555555"/></a>
  <a href="https://aider.chat/HISTORY.html"><img alt="Singularity" title="Percentage of the new code in Aider's last release written by Aider itself"
src="https://img.shields.io/badge/🔄%20Singularity-92%25-e74c3c?style=flat-square&labelColor=555555"/></a>
<!--[[[end]]]-->  
</p>

## Getting started
<!--[[[cog
# We can't "include" here.
# Because this page is rendered by GitHub as the repo README
cog.out(open("aider/website/_includes/get-started.md").read())
]]]-->

If you already have python 3.8-3.13 installed, you can get started quickly like this:

```bash
python -m pip install aider-install
aider-install

# Change directory into your code base
cd /to/your/project

# Work with DeepSeek via DeepSeek's API
aider --model deepseek --api-key deepseek=your-key-goes-here

# Work with Claude 3.7 Sonnet via Anthropic's API
aider --model sonnet --api-key anthropic=your-key-goes-here

# Work with GPT-4o via OpenAI's API
aider --model gpt-4o --api-key openai=your-key-goes-here

# Work with Sonnet via OpenRouter's API
aider --model openrouter/anthropic/claude-3.7-sonnet --api-key openrouter=your-key-goes-here

# Work with DeepSeek via OpenRouter's API
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=your-key-goes-here

# Work with Github Copilot
aider --model github_copilot/claude-3.7-sonnet-thought
```
<!--[[[end]]]-->

> [!TIP]
> If you have not authenticated with Github Copilot before, the first time you run Aider with the `github_copilot` model, you will be prompted to authenticate with Github Copilot using device code authentication. Follow the instructions in the terminal to authenticate.

See the
[installation instructions](https://aider.chat/docs/install.html)
and
[usage documentation](https://aider.chat/docs/usage.html)
for more details.

## Features

- Run aider with the files you want to edit: `aider <file1> <file2> ...`
- Ask for changes:
  - Add new features or test cases.
  - Describe a bug.
  - Paste in an error message or GitHub issue URL.
  - Refactor code.
  - Update docs.
- Aider will edit your files to complete your request.
- Aider [automatically git commits](https://aider.chat/docs/git.html) changes with a sensible commit message.
- [Use aider inside your favorite editor or IDE](https://aider.chat/docs/usage/watch.html).
- Aider works with [most popular languages](https://aider.chat/docs/languages.html): python, javascript, typescript, php, html, css, and more...
- Aider can edit multiple files at once for complex requests.
- Aider uses a [map of your entire git repo](https://aider.chat/docs/repomap.html), which helps it work well in larger codebases.
- Edit files in your editor or IDE while chatting with aider,
and it will always use the latest version.
Pair program with AI.
- [Add images to the chat](https://aider.chat/docs/usage/images-urls.html) (GPT-4o, Claude 3.5 Sonnet, etc).
- [Add URLs to the chat](https://aider.chat/docs/usage/images-urls.html) and aider will read their content.
- [Code with your voice](https://aider.chat/docs/usage/voice.html).
- Aider works best with Claude 3.7 Sonnet, DeepSeek V3, o1 & GPT-4o and can [connect to almost any LLM](https://aider.chat/docs/llms.html).


## Top tier performance

[Aider has one of the top scores on SWE Bench](https://aider.chat/2024/06/02/main-swe-bench.html).
SWE Bench is a challenging software engineering benchmark where aider
solved *real* GitHub issues from popular open source
projects like django, scikitlearn, matplotlib, etc.

## More info

- [Documentation](https://aider.chat/)
- [Installation](https://aider.chat/docs/install.html)
- [Usage](https://aider.chat/docs/usage.html)
- [Tutorial videos](https://aider.chat/docs/usage/tutorials.html)
- [Connecting to LLMs](https://aider.chat/docs/llms.html)
- [Configuration](https://aider.chat/docs/config.html)
- [Troubleshooting](https://aider.chat/docs/troubleshooting.html)
- [LLM Leaderboards](https://aider.chat/docs/leaderboards/)
- [GitHub](https://github.com/Aider-AI/aider)
- [Discord](https://discord.gg/Tv2uQnR88V)
- [Blog](https://aider.chat/blog/)


- *"My life has changed... There's finally an AI coding tool that's good enough to keep up with me... Aider... It's going to rock your world."* — [Eric S. Raymond](https://x.com/esrtweet/status/1910809356381413593)
- *"The best free open source AI coding assistant."* — [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *"The best AI coding assistant so far."* — [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *"Aider ... has easily quadrupled my coding productivity."* — [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *"It's a cool workflow... Aider's ergonomics are perfect for me."* — [qup](https://news.ycombinator.com/item?id=38185326)
- *"It's really like having your senior developer live right in your Git repo - truly amazing!"* — [rappster](https://github.com/Aider-AI/aider/issues/124)
- *"What an amazing tool. It's incredible."* — [valyagolev](https://github.com/Aider-AI/aider/issues/6#issue-1722897858)
- *"Aider is such an astounding thing!"* — [cgrothaus](https://github.com/Aider-AI/aider/issues/82#issuecomment-1631876700)
- *"It was WAY faster than I would be getting off the ground and making the first few working versions."* — [Daniel Feldman](https://twitter.com/d_feldman/status/1662295077387923456)
- *"THANK YOU for Aider! It really feels like a glimpse into the future of coding."* — [derwiki](https://news.ycombinator.com/item?id=38205643)
- *"It's just amazing. It is freeing me to do things I felt were out my comfort zone before."* — [Dougie](https://discord.com/channels/1131200896827654144/1174002618058678323/1174084556257775656)
- *"This project is stellar."* — [funkytaco](https://github.com/Aider-AI/aider/issues/112#issuecomment-1637429008)
- *"Amazing project, definitely the best AI coding assistant I've used."* — [joshuavial](https://github.com/Aider-AI/aider/issues/84)
- *"I absolutely love using Aider ... It makes software development feel so much lighter as an experience."* — [principalideal0](https://discord.com/channels/1131200896827654144/1133421607499595858/1229689636012691468)
- *"I have been recovering from multiple shoulder surgeries ... and have used aider extensively. It has allowed me to continue productivity."* — [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *"I am an aider addict. I'm getting so much more work done, but in less time."* — [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *"After wasting $100 on tokens trying to find something better, I'm back to Aider. It blows everything else out of the water hands down, there's no competition whatsoever."* — [SystemSculpt](https://discord.com/channels/1131200896827654144/1131200896827654149/1178736602797846548)
- *"Aider is amazing, coupled with Sonnet 3.5 it's quite mind blowing."* — [Josh Dingus](https://discord.com/channels/1131200896827654144/1133060684540813372/1262374225298198548)
- *"Hands down, this is the best AI coding assistant tool so far."* — [IndyDevDan](https://www.youtube.com/watch?v=MPYFPvxfGZs)
- *"[Aider] changed my daily coding workflows. It's mind-blowing how a single Python application can change your life."* — [maledorak](https://discord.com/channels/1131200896827654144/1131200896827654149/1258453375620747264)
- *"Best agent for actual dev work in existing codebases."* — [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
- *"One of my favorite pieces of software. Blazing trails on new paradigms!"* — [Chris Wall](https://x.com/chris65536/status/1905053299251798432)
- *"Aider has been revolutionary for me and my work."* — [Starry Hope](https://x.com/starryhopeblog/status/1904985812137132056)
- *"Try aider! One of the best ways to vibe code."* — [Chris Wall](https://x.com/Chris65536/status/1905053418961391929)
- *"Aider is hands down the best. And it's free and opensource."* — [AriyaSavakaLurker](https://www.reddit.com/r/ChatGPTCoding/comments/1ik16y6/whats_your_take_on_aider/mbip39n/)
- *"Aider is also my best friend."* — [jzn21](https://www.reddit.com/r/ChatGPTCoding/comments/1heuvuo/aider_vs_cline_vs_windsurf_vs_cursor/m27dcnb/)
- *"Try Aider, it's worth it."* — [jorgejhms](https://www.reddit.com/r/ChatGPTCoding/comments/1heuvuo/aider_vs_cline_vs_windsurf_vs_cursor/m27cp99/)
- *"I like aider :)"* — [Chenwei Cui](https://x.com/ccui42/status/1904965344999145698)
- *"Aider is the precision tool of LLM code gen... Minimal, thoughtful and capable of surgical changes to your codebase all while keeping the developer in control."* — [Reilly Sweetland](https://x.com/rsweetland/status/1904963807237259586)
- *"Cannot believe aider vibe coded a 650 LOC feature across service and cli today in 1 shot."* - [autopoietist](https://discord.com/channels/1131200896827654144/1131200896827654149/1355675042259796101)
- *"Oh no the secret is out! Yes, Aider is the best coding tool around. I highly, highly recommend it to anyone."* — [Joshua D Vander Hook](https://x.com/jodavaho/status/1911154899057795218)
- *"thanks to aider, i have started and finished three personal projects within the last two days"* — [joseph stalzyn](https://x.com/anitaheeder/status/1908338609645904160)
- *"Been using aider as my daily driver for over a year ... I absolutely love the tool, like beyond words."* — [koleok](https://discord.com/channels/1131200896827654144/1273248471394291754/1356727448372252783)
- *"aider is really cool"* — [kache (@yacineMTB)](https://x.com/yacineMTB/status/1911224442430124387)

- *The best free open source AI coding assistant.* -- [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *The best AI coding assistant so far.* -- [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *Aider ... has easily quadrupled my coding productivity.* -- [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *It's a cool workflow... Aider's ergonomics are perfect for me.* -- [qup](https://news.ycombinator.com/item?id=38185326)
- *It's really like having your senior developer live right in your Git repo - truly amazing!* -- [rappster](https://github.com/Aider-AI/aider/issues/124)
- *What an amazing tool. It's incredible.* -- [valyagolev](https://github.com/Aider-AI/aider/issues/6#issue-1722897858)
- *Aider is such an astounding thing!* -- [cgrothaus](https://github.com/Aider-AI/aider/issues/82#issuecomment-1631876700)
- *It was WAY faster than I would be getting off the ground and making the first few working versions.* -- [Daniel Feldman](https://twitter.com/d_feldman/status/1662295077387923456)
- *THANK YOU for Aider! It really feels like a glimpse into the future of coding.* -- [derwiki](https://news.ycombinator.com/item?id=38205643)
- *It's just amazing.  It is freeing me to do things I felt were out my comfort zone before.* -- [Dougie](https://discord.com/channels/1131200896827654144/1174002618058678323/1174084556257775656)
- *This project is stellar.* -- [funkytaco](https://github.com/Aider-AI/aider/issues/112#issuecomment-1637429008)
- *Amazing project, definitely the best AI coding assistant I've used.* -- [joshuavial](https://github.com/Aider-AI/aider/issues/84)
- *I absolutely love using Aider ... It makes software development feel so much lighter as an experience.* -- [principalideal0](https://discord.com/channels/1131200896827654144/1133421607499595858/1229689636012691468)
- *I have been recovering from multiple shoulder surgeries ... and have used aider extensively. It has allowed me to continue productivity.* -- [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *I am an aider addict. I'm getting so much more work done, but in less time.* -- [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *After wasting $100 on tokens trying to find something better, I'm back to Aider. It blows everything else out of the water hands down, there's no competition whatsoever.* -- [SystemSculpt](https://discord.com/channels/1131200896827654144/1131200896827654149/1178736602797846548)
- *Aider is amazing, coupled with Sonnet 3.5 it’s quite mind blowing.* -- [Josh Dingus](https://discord.com/channels/1131200896827654144/1133060684540813372/1262374225298198548)
- *Hands down, this is the best AI coding assistant tool so far.* -- [IndyDevDan](https://www.youtube.com/watch?v=MPYFPvxfGZs)
- *[Aider] changed my daily coding workflows. It's mind-blowing how a single Python application can change your life.* -- [maledorak](https://discord.com/channels/1131200896827654144/1131200896827654149/1258453375620747264)
- *Best agent for actual dev work in existing codebases.* -- [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
