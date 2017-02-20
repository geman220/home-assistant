#!/usr/bin/env python
import logging
import requests

from homeassistant.components.lock import LockDevice
from homeassistant.const import (STATE_LOCKED, STATE_UNLOCKED, STATE_UNKNOWN, CONF_DEVICE, CONF_ACCESS_TOKEN)

import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import (PLATFORM_SCHEMA)
import voluptuous as vol

# Required Parameters for Lockitron lock component instance
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICE): cv.string,
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
})

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Demo lock platform."""
    add_devices([Lockitron(config.get(CONF_ACCESS_TOKEN), config.get(CONF_DEVICE))])

class Lockitron(LockDevice):
    """Representation of a Demo lock."""
    def __init__(self, access_token, device_id):
        """Initialize the lock."""
        self._apiurl = 'https://api.lockitron.com'
        self.device_id = device_id
        self.access_token = access_token
        self._state = STATE_UNKNOWN
        self._name = 'Lockitron' # TODO: Get this from JSON

    @property
    def should_poll(self):
        """No polling needed for a demo lock."""
        return True

    @property
    def name(self):
        """Return the name of the lock if any."""
        return self._name

    @property
    def is_locked(self):
        """Return true if lock is locked."""
        url = '{}/v2/locks/{}?access_token={}'.format(
            self._apiurl,
            self.device_id,
            self.access_token)
        response = requests.get(url)
        data = response.json()

        if data.get('state'):
            return data['state'] == 'lock'
        else:
            _LOGGER.error("LOCKITRON: Response: %s" + str(data))
            return UNKNOWN


    def lock(self, **kwargs):
        """Lock the device."""
        url = '{}/v2/locks/{}?access_token={}'.format(
            self._apiurl,
            self.device_id,
            self.access_token)
        ret = requests.put(url,  data = {'state':'lock'})
        self._state = STATE_LOCKED
        self.schedule_update_ha_state()
        return ret.json()


    def unlock(self, **kwargs):
        """Unlock the device."""
        url = '{}/v2/locks/{}?access_token={}'.format(
            self._apiurl,
            self.device_id,
            self.access_token)
        ret = requests.put(url,  data = {'state':'unlock'})
        self._state = STATE_UNLOCKED
        self.schedule_update_ha_state()
        return ret.json()
