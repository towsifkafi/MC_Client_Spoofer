# Brand Strip Minecraft Proxy

This is a python script that proxies a Minecraft server and modifies plugin message packets sent by the client to change its name and brand. It can also block out specified packets if they have a keyword match.

🙄 *Some minecraft server banned me for using a normal client. so i managed to make this to send different client name to the server.*

## Requirements

- Python 3.6 or higher
- `twisted`, `quarry`, `colorama` library (to install: `pip3 install twisted quarry colorama`)

## Usage

To run the proxy, use the command below:

```python
python3 brand_strip.py -b <connect_ip> -q <connect_port>
```

where `<connect_ip>` and `<connect_port>` is the ip/port of the Minecraft server you want to connect to.

You may also specify other options such as the listen address and port, and the connect address, using the following arguments:

```python
 -a, --listen-host: address to listen on (default: `0.0.0.0`)
 -p, --listen-port: port to listen on (default: `25565`)
 -b, --connect-host: address to connect to (default: `127.0.0.1`)
 -q, --connect-port: port to connect to (required)
```

For example, to listen on `localhost` port `12345` and connect to `example.com` on port `25565`, use the command below:

```python
python3 brand_strip.py -a localhost -p 12345 -b example.com -q 25565
```

## Functionality

The proxy intercepts plugin message packets sent by the client and modifies them to change the client's name and brand. Specifically, it replaces instances of `LiteLoader` in the packet data with `Lunarclient:v2.7.1-2324` or replaces instances of `cmclient:f1df6c8` with `NiceClient:1337`.

The proxy also checks each packet against a list of keywords, and blocks the packet if any of the keywords match. The keywords to check for can be modified within the script by changing the `strings_to_check` list.

All intercepted packets are logged to the console, along with their direction (upstream or downstream), identifier, and data. Modified packets are highlighted in cyan, blocked packets are highlighted in red, and upstream/downstream packets are highlighted in blue/magenta, respectively.

## Credits

It makes use of the `quarry` library by David Vierra and the `twisted` library by Twisted Matrix Laboratories. Also thanks to [LiveOverflow](https://github.com/LiveOverflow/minecraft-hacked) for [I Spent 100 Days Hacking Minecraft](https://www.youtube.com/watch?v=Ekcseve-mOg).
