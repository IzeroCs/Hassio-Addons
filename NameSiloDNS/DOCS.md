# Home Assistant Community Add-on: Namesilo DNS IP
Namesilo DNS IP is used to get the Public IP of the network router and update the DNS Record
automatically for the domain you want to point to the router. Every time the router is rebooted, its Public IP will change. If you buy a static Public IP from a network operator, you have to pay a large fee, so using this method is both simple and economical.
## Installation

The installation of this add-on is pretty straightforward and not different in comparison to
installing any other Home Assistant add-on.

1. Click the Home Assistant My button below to open the add-on on your Home Assistant instance.

   [![Open this add-on in your Home Assistant instance.][addon-badge]][addon]

1. Click the "Install" button to install the add-on.
1. Start the "Namesilo DNS IP" add-on
1. Check the logs of the "Namesilo DNS IP" add-on to see if everything went well.

## Configuration
**Note**: _Remember to restart the add-on when the configuration is changed._
Example add-on configuration:

```yaml
log: true
api: api-token-namesilo
domain: domain-in-namesilo.com
ttl: 3603
records:
    - "@"
    - "www"
interval_update: 30
```
**Note**: _This is just an example, don't copy and past it! Create your own!_
### Option: `log`
The `log` is the addon log addon option, which is useful when you
need to deal with an unknown issue. The value is true to enable logging, and false to disable logging.
### Option: `api`
The `api` is the key generated in the control panel of [NameSilo](namesilo.com),
you go to **`Account Home Page`** > **`API manager`** > **`API Key`** >
**`Check:`** *`Submitting this form your acceptance of our API terms of use`* >
**`Generate`**. Then you copy the api code you just created into the configuration.
### Option: `domain`
The `domain` is the domain name you registered from [NameSilo](namesilo.com)
### Option: `ttl`
The `ttl` is optional for all TTL Records
### Option: `records`
The `records` is a list of how to prefix a domain's hostname, for example:
- `@` => `domain.com`
- `www` => `www.domain.com`
- `subdomain` is `subdomain.domain.com`

**Note**: _You only need to enter the prefix, not use the prefix.domain.com_
### Option: `interval_update`
The `interval_update` is the time to repeat the check and update, in seconds,
which must be greater than or equal to 10 seconds.

[addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[addon]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=ee21dcf3_namesilo_dns_auto
