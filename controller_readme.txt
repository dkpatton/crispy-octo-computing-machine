# Here's a full summary you can paste into your game's config or README:

# --- Joystick Device Summary ---

DEVICE NAME: "SWITCH CO.,LTD. Controller (Dinput)"
USB ID: 2563:0575 (ShenZhen ShanWan Technology Co., Ltd. ZD-V+ Wired Gaming Controller)
USB BUS: Bus 001 Device 002

# Linux Device Paths:
- Joystick interface: /dev/input/js0
- Event interface (for SDL/game engines): (determine with `udevadm`, example: /dev/input/event12 or /dev/input/event13)

# Capabilities:

AXES (6 axes):
0: X          # Left stick horizontal
1: Y          # Left stick vertical
2: Z          # Right trigger or unknown (check mapping)
3: Rz         # Right stick horizontal
4: Hat0X      # D-pad horizontal (left/right)
5: Hat0Y      # D-pad vertical (up/down)

BUTTONS (13 buttons):
0: BtnA       # A button
1: BtnB       # B button
2: BtnC       # C button (may be unused, test)
3: BtnX       # X button
4: BtnY       # Y button
5: BtnZ       # Z button (may be unused)
6: BtnTL      # Left bumper (L1)
7: BtnTR      # Right bumper (R1)
8: BtnTL2     # Left trigger (L2)
9: BtnTR2     # Right trigger (R2)
10: BtnSelect # Select / Back
11: BtnStart  # Start
12: BtnMode   # Mode / Guide / Home

# Notes:
- Tested via `jstest /dev/input/js0`
- Detected and functional in Linux kernel joystick API (version 2.1.0)
- No special drivers needed (standard USB HID joystick support)

# To programmatically read the event interface (e.g. for SDL2):

sudo udevadm info -q all -n /dev/input/js0 | grep event
# Example output: E: DEVNAME=/dev/input/event12
# Then use /dev/input/event12 for SDL_OpenJoystickDevice() or similar.

# END SUMMARY
