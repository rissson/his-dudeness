Here is a basic log file name :

`assets/logs/[year]_[month]_[day]__[hour]_[minute]_[second].log`

Here is a basic log message :

`[timestamp] :: [type] :: [number] :: [file_name] :: [message]`

Here is how you should log things :
```
from logs.logs import log
log(20, '0000', 'tabs/TabServer/TabServer/quit', 'quitting TabServer', object1, object2)
```

The first parameter is the type of message, for more infos, please refer to logs.logs.log documentation.

The next 4-digits number will give you quick informations, see below :

Numbers used :

The number is always a 4-digits number. The first three digits indicates where it comes from (the class) and the last digit indicates some more information.

- main.py and special informations (platform, python version, modules version...) : `-1`
- imports : `0000`
- Borg : `0001`
- inputs : `0002`
- display : `0003`
- menu : `0004`
- pygame (such as `pygame.init()`) : `0005`
- graphalama : `1...`
    * `__init__` : `1000`
    * Carac : `110.`
    * Text : `111.`
    * TextBox : `112.`
    * SText : `113.`
    * FlyingText : `114.`
    * Rectangle : `120.`
    * Area : `121.`
    * Circle : `130.`
    * Color : `140.`
    * MetaClassFont : `150.`
    * Font : `151.`
    * StatesButtons : `160.`
    * ListCell : `170.`
    * StringListCell : `171.`
    * ListView : `172.`
    * ScrollBar : `180.`
    * DiegoScrollBar : `181.`
    * Photo : `190.`
    * PhotoList : `191.`
    * Icon : `192.`
    * other stuff : `101.`
- conns : `2...`
    * Conns : `200.`
    * Ftp : `210.`
    * Ftp-Callback : `211.`
    * MySQL : `220.`
    * SQLite : `221.`
    * Profile : `230.`
- random stuff : `3...` or `4...`
    * crypto : `300.`
    * trad : `310.`
    * params : `320.`
    * error_screen : `3300`
    * wait_party : `3342`
    * graphalama/functions : `340.`
    * graphalama/CONSTANTS : `341.`
    * bug : `350.`
- tabs : `5...`
    * Super : `500.`
    * Home : `510.`
        - Weather : `511.`
    * Lama : `520.`
    * Mails : `530.`
    * Messages : `540.`
        - OldMessages : `541.`
        - OldMessage : `542.`
        - ConvoSelect : `543.`
    * Music : `550.`
        - to
        - be
        - completed
    * Params : `321.`
    * Photos : `570.`
    * Server : `580.`
        - TabInServer : `581.`
    * Stats : `590.`
    * Wunderlist : `560.`
    
here is how you should complete the last digit, depending on what function you're in :
`__init__` : `...0`
normal function : `...1`
`run` : `...4`
`__quit__` : `...9`
`@staticmethod` : `...2`
`@property` : `...3`
functions for the buggy minute : `...5`
