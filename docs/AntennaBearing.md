# Antenna Bearing

Open **Station → Control Devices → Antenna Bearing**. Set the station grid in
Station Settings, then enter a destination Maidenhead grid. The planner
calculates short- and long-path true bearings from the grid centers and shows
the short-path distance. Use the grid from the map or QSO when known.
Coincident and antipodal centers do not define a unique bearing.

For controller readback, enter a rotctld host and port and select
**Read Position**. The request runs once and has a three-second timeout.
A reading expires after 30 seconds, and changing the host or port clears it.
Azimuth and elevation are shown in the controller's own frame. Azimuth can
exceed 360° for controllers with mechanical overlap. An azimuth-only
controller may omit elevation.

HermitSDR sends only the position query. Rotctld itself uses plain TCP
without authentication, so use a trusted local daemon or a local tunnel.
The wire command follows the Hamlib Extended Response Protocol.
[Hamlib rotctld manual](https://hamlib.sourceforge.net/html/rotctld.1.html)
