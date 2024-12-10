# Dawarich Home Assistant Integration

> [!NOTE]
> This is an experimental integration for Dawarich, expect possibly breaking changes. This is a community integration, not affiliated by Dawarich.

[Dawarich](https://dawarich.app/) is a self-hosted Google Timeline alternative.

This integration does two things, of which one is optional.
1. It provides statistics for your account, this includes total distance in kilometers, number of cities visited etc.
2. (optional) You can set a device tracker (mobile phone for example) to send it's data through home assistant to Dawarich. That way you won't need another app, and can simply use the, probably already existing, location in HA.

## Install
There are two ways to install this. The easiest is with [HACS](https://hacs.xyz/).

### Install with HACS

<!-- #### HACS Installed and if this is added to HACS repository.
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=AlbinLind&repository=dawarich-home-assistant) -->

<!-- #### HACS not Installed -->
Altough the below instructions might look complicated, they are rather simple.
1. Make sure you have HACS installed, ([instructions](https://hacs.xyz/docs/use/))
2. Navigate to HACS in your Home Assistant.
3. Press the three buttons in the top right.
4. Choose Custom Repository
5. Paste the link to the repository `https://github.com/AlbinLind/dawarich-home-assistant`.
6. Choose Type: `Integration`.
7. Search for `Dawarich` and press install
8. Restart Home Assistant
9. Navigate to `Settings -> Devices & services` and add a Dawarich instance.

### Manual Installation
Take the items under `custom_components/dawarich` and place them in the folder `homeassistant/custom_components/dawarich`.
