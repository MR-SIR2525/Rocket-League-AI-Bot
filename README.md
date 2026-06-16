![image](https://github.com/MarlBurroW/RLMarlbot/assets/3024430/68bcbce7-545a-4ae6-b3b7-ab44fae8ad55)


# RLMarlbot

Bot player based on my [python SDK](https://github.com/MarlBurroW/RLSDK-Python) and RLBot standard.
I recommend to look at the RLSDK-Python repository to understand how the bot works.

## Disclaimer

⚠️⚠️⚠️ RLMarlbot is designed to facilitate the use of bots in private matches with your friends without the need for RLBot. It should be used primarily for testing and debugging by botmakers. However, this tool employs advanced reverse engineering techniques that could legitimately be considered cheating by the game's standards. I strongly advise against using RLMarlbot in ranked or casual matches. Your Rocket League account is likely to be banned quickly if you violate this rule.

## Requirements
- [Poetry](https://python-poetry.org/) to install dependencies
- RocketLeague Epic (x64) running
- Python 3.11.0 (x64)
- Pyinstaller if you want to build the exe


## CLI Options

```
usage: main.py [-h] [-p PID] [-b BOT] [--kickoff] [--minimap] [--monitoring] [--debug-keys] [--clock] [--debug]

RLMarlbot

options:
  -h, --help         show this help message and exit
  -p PID, --pid PID  Rocket League process ID
  -b BOT, --bot BOT  Bot to use (nexto, necto, seer, element)
  --kickoff          Override all bots kickoff with a default one that is pretty good. 1 to enable, 0 to disable
  --minimap          Enable minimap
  --monitoring       Enable monitoring
  --debug-keys       Print all keys pressed in game in the console (Gamepad and Keyboard)
  --clock            Sync ticks with an internal clock at 120Hz, can help in case of unstable FPS ingame
  --debug            Show debug information in the console
```


## Installation

```bash	
# Clone the repository
git clone https://github.com/MarlBurroW/RLMarlbot

# Change directory
cd RLMarlbot

# Install dependencies (requires Poetry and Python 3.11 x64)
poetry install

# Enter poetry shell
poetry shell

# Run the game (Rocket League Epic x64) before starting the bot.
# From repo root:
poetry run python rlmarlbot/main.py
```

## Build binary from source

```bash
pyinstaller .\main.spec
```

## Updates
If the repo is not up to date, you must git pull and update dependencies:
```bash
# get latest changes
git pull
# Update dependencies
poetry install
```


## Memory Writer
Source of the memory writer is in the folder `MemoryWriter`. You need to build it and place the output in `rlmarlbot/memory_writer/`:

1. Open `MemoryWriter/MemoryWriter.sln` in Visual Studio.
2. Set configuration to **Release | x64** (Rocket League is 64-bit).
3. Configure Python 3.11 include and lib paths for pybind11 if needed (see project properties).
4. Build; the project outputs to `rlmarlbot/memory_writer/memory_writer.pyd`.
5. Run the bot from the **repo root** so `memory_writer` can be imported (e.g. `poetry run python rlmarlbot/main.py`).

If the bot starts but does not control the car, the game may have been updated and the **input offset** may have changed. Edit `config.json` and set `"input_offset"` to the new value (decimal, e.g. `2448` for `0x0990`, or hex string `"0x0990"`). Re-find the FVehicleInputs offset (e.g. with Cheat Engine / ReClass) from the player controller if needed.

## Game updates and RLSDK
If the bot fails to attach or gets no game data (e.g. "No game event", "No local players"), the game build may have changed and **rlsdk-python**’s internal offsets (GNames, GObjects, etc.) may be outdated. Check for a newer [rlsdk-python](https://pypi.org/project/rlsdk-python/) version or the [AScriver/RLSDK-Python](https://github.com/AScriver/RLSDK-Python) fork for updates; then run `poetry update rlsdk-python` or adjust the version in `pyproject.toml`.

## How does it works ?

RLMarlbot is a bot that uses the RLSDK Python package to read data from RocketLeague.exe. It uses the data to build a GameTickPacket (Structure of data defined by RLBot framework) and put the data into the Nexto RLBot agent. The Agent compute data in the AI torch model and return a SimpleControllerState that contains the car inputs data. Then inputs are written in the game memory with a native python library written in C++ (memory_writer.pyd) to be able to overwrite car inputs faster than the game loop.


## Credits

- **Rolv-Arild** - Necto/Nexto model + RLBot agent
- **Kxqs**: For his discord management, his good ideas and his feedback
- **Thorami**: For giving me some very useful tips, especially on how to obtain the base addresses of GNames and GObjects.
- **Kandda**: Made the Marlbot logo
- **RLBot**: For having created a standard interface for bot creation.
- **Bardak**: For testing
- **AScriver**: Contribute to improve the RLSDK
