A logging bot for XMPP chat rooms.

# What?
* XMPP Log bot
* Search interface (with whoosh and flask)
* Log to text files

# Install

    pip install logbot

# Running

    logbot \
        --host chat.looney.org \
        --user logbot@chat.looney.org \
        --passwd  S3cr3t \
        yada@conference.looney.org

Web interface at [http://localhost:5000](http://localhost:5000)

# Bugs

Version 0.3.0 changed search schema. Please run `utils/upgrade_03.py` to update
the schema.

# Contact
Miki Tebeka <miki.tebeka@gmail.com>

Bugs go [here](https://bitbucket.org/tebeka/logbot/issues)

<!---
vim: spell
-->
