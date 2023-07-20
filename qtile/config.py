# import libraries
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from thingsiplay.widget import output
import os
import subprocess

# modkey
mod = "mod4"

# default terminal command
# terminal = "kitty tmux new-session -A -s main"
terminal = "kitty"

# default file manager
fm = "thunar"

# keybindings
keys = [
    # resize windows
    Key([mod], "l", lazy.layout.grow_main()),
    Key([mod], "h", lazy.layout.shrink_main()),

    Key([mod], "j", lazy.layout.next()),
    Key([mod], "k", lazy.layout.previous()),

    # move windows around
    Key([mod], "Return", lazy.layout.swap_main()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Return", lazy.layout.flip()),

    # banish cursor
    Key([mod], "x", lazy.spawn("xdotool mousemove 2560 1440")),

    # launch dmenu
    Key([], "XF86LaunchA", lazy.spawn("dmenu_run")),

    # launch terminal
    Key([mod], "1", lazy.spawn(terminal)),

    # launch firefox
    Key([mod], "2", lazy.spawn("firefox")),

    # launch thunar
    Key([mod], "3", lazy.spawn(fm)),

    # rssguard
    Key([mod], "4", lazy.spawn("rssguard")),

    # launch flameshot
    Key([mod], "0", lazy.spawn("flameshot gui")),

    # cycle through enabled layouts
    Key([mod], "Tab", lazy.next_layout()),

    # kill window
    Key([mod, "shift"], "c", lazy.window.kill()),

    # reload configuration
    Key([mod, "control"], "r", lazy.reload_config()),

    # quit qtile
    Key([mod, "control"], "q", lazy.shutdown()),

    # volume controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # media keys
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    Key(["shift"], "XF86AudioNext", lazy.spawn("mpc seekthrough +00:00:05")),
    Key(["shift"], "XF86AudioPrev", lazy.spawn("mpc seekthrough -00:00:05")),

    # brightness controls
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +1")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 1-")),
    Key([mod], "XF86MonBrightnessUp", lazy.spawn("sct 4500")),
    Key([mod], "XF86MonBrightnessDown", lazy.spawn("sct 5500")),

    # screen locking
    Key([], "XF86Eject", lazy.spawn("mpc pause"), lazy.spawn("brightnessctl set 0"), lazy.spawn("i3lock --color 000000")),
    Key(["shift"], "XF86Eject", lazy.spawn("brightnessctl set 10")),
    Key([mod, "shift"], "XF86Eject", lazy.spawn("sudo reboot")),
    Key([mod, "control"], "XF86Eject", lazy.spawn("sudo poweroff")),

    # other commands
    KeyChord([mod], "e", [
        # toggle bar visibility
        Key([], "b", lazy.hide_show_bar()),

    ]),
]

groups = [Group(i) for i in "asdf"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.MonadTall(
        border_width=3,
        border_normal="212121",
        border_focus='770000',
        align=0,
        margin=10,
    ),
    layout.MonadWide(
        border_width=3,
        border_normal="212121",
        border_focus='770000',
        align=0,
        margin=10,
    ),
    layout.TreeTab(
        active_bg='ffffff',
        active_fg='000000',
        inactive_bg='000000',
        inactive_fg='737373',
        bg_color='000000',
        panel_width=300,
        previous_on_rm=True,
        font="Libertinus Sans",
        sections=['']
    ),
]

widget_defaults = dict(
    font="Libertinus Sans",
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

background = ["#b58900", "#826200"]
foreground = "#fdf6e3"
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    padding=5,
                    highlight_method="block"
                ),
                widget.Sep(
                    foreground=foreground,
                    linewidth=1,
                    size_percent=50,
                ),
                widget.WindowTabs(
                    separator="     ",
                    padding=5,
                    foreground=foreground
                ),
                output.Output(
                    update_interval=60,
                    cmd="uptime --pretty",
                    padding=5,
                    background=background,
                    foreground=foreground,
                ),
                widget.Sep(
                    foreground=foreground,
                    background=background,
                    linewidth=1,
                    size_percent=50,
                ),
                output.Output(
                    update_interval=5,
                    cmd="nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2",
                    fmt="Network: {}",
                    padding=5,
                    background=background,
                    foreground=foreground,
                ),
                widget.Sep(
                    foreground=foreground,
                    background=background,
                    linewidth=1,
                    size_percent=50,
                ),
                widget.Backlight(
                    background=background,
                    foreground=foreground,
                    padding=5,
                    fmt="Backlight: {}"
                ),
                widget.Sep(
                    foreground=foreground,
                    background=background,
                    linewidth=1,
                    size_percent=50,
                ),
                output.Output(
                    background=background,
                    foreground=foreground,
                    padding=5,
                    update_interval=0.25,
                    cmd='pamixer --get-volume',
                    fmt='Volume: {}',
                ),
                widget.Mpd2(
                    background=["#859900", "#596600"],
                    foreground=foreground,
                    status_format='{play_status} {artist}/{title}',
                    idle_format='{play_status} {idle_message}',
                    idle_message='MPD not playing',
                    padding=5,
                ),
                widget.Clock(
                    format='%d/%m/%y %H:%M',
                    padding=5,
                ),
                widget.Sep(
                    foreground=foreground,
                    linewidth=1,
                    size_percent=50,
                ),
                widget.Systray(
                    icon_size=12,
                    padding=5,
                ),
                widget.CurrentLayoutIcon(
                    scale=0.6,
                    padding=5,
                ),
            ],
            24,
            # background=["#434343", "#000000"],
            background=["#000000", "#454649"],
            # background=["#4d4b45", "#3f3e3a"],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')    
    # Insert your autostart script here
    subprocess.Popen([home + '/documents/scripts/shell/autostart.sh'])

