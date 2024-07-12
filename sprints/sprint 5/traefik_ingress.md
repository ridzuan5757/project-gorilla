# `traefik`

`traefik` is an open-source edge router that enable `Services` to be published.
It receives requests on behlf of the system and finds out which components are
responsible for handling them.

`traefik` is based on the concept of `EntryPoints`, `Routers`, `Middlewares`,
and `Services`. The main features include dynamic configuration, automatic
service discovery, and support for multiple backends and protocols.
- `EntryPoints` are the network entry points into `traefik`. They define the
  port which will receive the packets, and whether to listen for TCP or UDP.

