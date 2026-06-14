"""Physical and mission constants.

NASA-sourced facts are tagged [NASA] with their origin. Everything else is a
standard physical constant or a clearly labelled mission assumption (TBR).

Sources:
    NASA VIPER Lunar Operations - Earth invisible ~14 days/month (libration);
        direct-to-Earth via the Deep Space Network.
    NASA SCaN LCRNS ("Blazing a Trail to Lunar Relays") - relay required when a
        surface asset is not in line of sight with Earth.
"""

# ---- Physical constants ----
C_KM_S: float = 299_792.458       # speed of light, km/s
EARTH_MOON_KM: float = 384_400.0  # mean Earth-Moon distance, km
MU_MOON: float = 4902.8           # lunar gravitational parameter, km^3/s^2
R_MOON_KM: float = 1737.4         # lunar mean radius, km

# ---- NASA-sourced mission facts ----
BLACKOUT_DAYS: float = 14.0       # [NASA VIPER] Earth invisible per ~29.5-day month
LUNAR_CYCLE_DAYS: float = 29.5    # mission duration, one lunar cycle (MR-01)

# ---- Mission assumptions (TBR - to be confirmed in Phase A) ----
DEFAULT_DAILY_DATA_MB: float = 50.0    # science + engineering data per day (estimate)
DEFAULT_RELAY_ALT_KM: float = 100.0    # low lunar relay orbiter altitude (TBR)
DEFAULT_DOWNLINK_BPS: float = 256_000  # conservative DTE/relay rate, bits/s (TBR)

# Requirement under test (MR-06)
MR06_LATENCY_HOURS: float = 48.0       # max data latency requirement (TBR)
