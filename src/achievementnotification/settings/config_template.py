CONFIG_TEMPLATE = """{
    // To generate default config, delete config file and launch a game again

    // Global features toggle
    // Valid values: true/false (default: true)
    //
    // When set to false, it globally disables all features of this mod
    // however it does not remove mod presence itself. 
    "enabled": %(enabled)s,

    // Valid values: number between 0.2 and 4.0 (default 1.0)
    // 
    // Controls scale of the entire notification widget.
    "scale": %(scale)s,

    // Valid values: ["compact", "detailed"]
    // Default value: "detailed"
    //
    // Configures display mode of achievement mod:
    // - "compact"  - displays small icon, name of achievement and short description,
    // - "detailed" - displays big icon, name of achievement and detailed description.
    "display-mode": %(display-mode)s,

    // Valid values: number between 0.0 and 1.0 (default 0.8)
    // 
    // Controls vertical position of achievement mod, relative to screen height:
    // - 0.0 means top side,
    // - 1.0 means bottom side.
    "vertical-position": %(vertical-position)s,

    // Valid values: number between 0.5 and 10.0 (default 5.0)
    //
    // Controls how long should achievement be displayed.
    // For multiple achievements at once, this time applies only to first achievement in group.
    // The other achievements in group uses "consecutive-display-time" parameter.
    "first-display-time": %(first-display-time)s,

    // Valid values: number between 0.5 and 10.0 (default 3.0)
    //
    // If multiple achievements occurred at once, this parameter controls
    // how long should consecutive achievements in group (after first one) be displayed.
    "consecutive-display-time": %(consecutive-display-time)s,

    // For each achievement
    // Valid values: true/false (default: true)
    //
    // When set to true, displays that achievement when it's condition is met during battle.
    "achievements": {
        "arsonist": %(achievements-arsonist)s,
        "bonecrusher": %(achievements-bonecrusher)s,
        "charmed": %(achievements-charmed)s,
        "defender": %(achievements-defender)s,
        "demolition": %(achievements-demolition)s,
        "duelist": %(achievements-duelist)s,
        "even": %(achievements-even)s,
        "fighter": %(achievements-fighter)s,
        "heroesOfRassenay": %(achievements-heroesOfRassenay)s,
        "huntsman": %(achievements-huntsman)s,
        "impenetrable": %(achievements-impenetrable)s,
        "ironMan": %(achievements-ironMan)s,
        "kamikaze": %(achievements-kamikaze)s,
        "mainGun": %(achievements-mainGun)s,
        "medalAntiSpgFire": %(achievements-medalAntiSpgFire)s,
        "medalBurda": %(achievements-medalBurda)s,
        "medalCoolBlood": %(achievements-medalCoolBlood)s,
        "medalDumitru": %(achievements-medalDumitru)s,
        "medalGore": %(achievements-medalGore)s,
        "medalHalonen": %(achievements-medalHalonen)s,
        "medalLafayettePool": %(achievements-medalLafayettePool)s,
        "medalLehvaslaiho": %(achievements-medalLehvaslaiho)s,
        "medalNikolas": %(achievements-medalNikolas)s,
        "medalOrlik": %(achievements-medalOrlik)s,
        "medalOskin": %(achievements-medalOskin)s,
        "medalStark": %(achievements-medalStark)s,
        "medalPascucci": %(achievements-medalPascucci)s,
        "medalRadleyWalters": %(achievements-medalRadleyWalters)s,
        "medalTamadaYoshio": %(achievements-medalTamadaYoshio)s,
        "scout": %(achievements-scout)s,
        "shootToKill": %(achievements-shootToKill)s,
        "steelwall": %(achievements-steelwall)s,
        "sturdy": %(achievements-sturdy)s,
        "supporter": %(achievements-supporter)s,
        "warrior": %(achievements-warrior)s
    },

    // DO NOT touch "__version__" field
    // It is used by me to seamlessly update config file :)
    "__version__": 2
}"""
