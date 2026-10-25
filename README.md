# Rocket League AI Bot

Rocket League AI Bot is a Python runner for RLBot-style agents that reads Rocket League state through `rlsdk-python`, builds RLBot `GameTickPacket` structures, runs bot policies such as Nexto, Necto, Seer, Element, or Immortal, and writes controller input back to the game through a native memory writer.

This project is intended for private matches, bot development, debugging, and experimentation.

## Important Disclaimer

This tool reads and writes Rocket League process memory. Using it in public, ranked, casual, or otherwise unauthorized online matches can be considered cheating and may get an account banned. Use it only in private, controlled environments where bot tooling is allowed.

## Features

- Runs multiple bundled bot agents: Nexto, Necto, Seer, Element, and Immortal.
- Reads game state through RLSDK and converts it to RLBot packet structures.
- Writes controller input through `memory_writer.pyd`.
- Optional minimap, monitoring output, debug keys, debug logs, and 120 Hz clock mode.
- Optional built-in kickoff override.
- Configurable toggle keys and game input offset through `config.json`.
- PyInstaller spec for building a standalone executable.

## Requirements

- Windows x64.
- Rocket League Epic x64 running.
- Python 3.11 x64.
- Poetry.
- Visual Studio if rebuilding the native `MemoryWriter` extension.
- PyInstaller if building an executable.

## Install

```bash
poetry install
```

If Poetry creates a virtual environment, run commands through `poetry run`.

## Memory Writer

The bot needs the native memory writer module at:

```text
rlmarlbot/memory_writer/memory_writer.pyd
```

Source for the native module lives in `MemoryWriter/`.

Build steps:

1. Open `MemoryWriter/MemoryWriter.sln` in Visual Studio.
2. Select `Release | x64`.
3. Configure Python 3.11 include and library paths for pybind11 if needed.
4. Build the solution.
5. Confirm the output is copied to `rlmarlbot/memory_writer/memory_writer.pyd`.

Run the bot from the repository root so the `memory_writer` module can be imported.

## Run

Start Rocket League first, then run:

```bash
poetry run python -m rlmarlbot
```

Choose a bot interactively or pass one with `--bot`:

```bash
poetry run python -m rlmarlbot --bot nexto
```

Useful options:

```text
-p, --pid PID        Rocket League process ID
-b, --bot BOT        Bot to use: nexto, necto, seer, element, immortal
--kickoff            Use the built-in kickoff override
--minimap            Enable minimap
--monitoring         Print monitoring information
--debug-keys         Print gamepad and keyboard input events
--clock              Sync ticks with a Python 120 Hz clock
--debug              Print debug information
--nexto-beta VALUE   Beta value passed to Nexto
```

## Configuration

On first run, the bot writes a default `config.json`:

```json
{
  "bot_toggle_key": "F1",
  "dump_game_tick_packet_key": "F2",
  "input_offset": 2448
}
```

`input_offset` may be specified as a decimal integer or a hex string such as `"0x0990"`.

If the bot starts but does not control the car after a game update, the `FVehicleInputs` offset may have changed. Re-find the input offset from the player controller and update `config.json`.

## Build an Executable

```bash
poetry run pyinstaller .\main.spec
```

The spec includes the bundled bot folders, model files, helper module, and native memory writer.

## Troubleshooting

- If the SDK cannot attach, confirm Rocket League Epic x64 is running.
- If `memory_writer` cannot import, confirm `memory_writer.pyd` exists under `rlmarlbot/memory_writer/` and matches Python 3.11 x64.
- If there is no game data after an update, `rlsdk-python` offsets may need an update.
- If the car does not respond, check `input_offset` in `config.json`.
- If the bot selected is not recognized, use one of `nexto`, `necto`, `seer`, `element`, or `immortal`.

## How It Works

1. RLSDK reads live Rocket League objects from `RocketLeague.exe`.
2. The runner converts that state into RLBot-compatible packet structures.
3. The selected bot returns a `SimpleControllerState`.
4. The memory writer writes that controller state to the current player input structure.

## Credits

- Rolv-Arild for Necto/Nexto model and RLBot agent work.
- Kxqs for feedback and community support.
- Thorami for tips on game addresses and object discovery.
- Kandda for the Marlbot logo.
- RLBot for the bot interface standard.
- Bardak for testing.
- AScriver for RLSDK improvements.
