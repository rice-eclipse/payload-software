# payload-software
A most descriptive name.

### Setting up the MainSoftwareSystem.

Clone the repository.
`git clone https://github.com/rice-eclipse/payload-software.git`

"cd" into the payload-software directory. Example:

`cd payload-software`

Create and active a local venv.

`python -m venv venv`

`source venv/bin/activate` (Linux, macOS, *nix Terminal Emulator)

`venv\Scripts\activate` (Windows cmd)

`venv\Scripts\Activate.ps1` (Windows Powershell)

Note: If you are on Windows and the venv commands don't seem to work, try the following commands.

`.venv\Scripts\activate` (Windows cmd)

`.venv\Scripts\Activate.ps1` (Windows Powershell)

Install dependencies.

(If on the Raspberry Pi, open requirements.txt and uncomment the `picamera==1.13` line before running the following command.)

`pip install -r requirements.txt`

The software system should now be ready to go.

### Running the MainSoftwareSystem.

"cd" into the payload-software directory. Example:

`cd payload-software`

Pull latest updates.

`git pull`

Depending on what version is the most active and feature complete, checkout the appropriate branch.
If it is unknown which is more up-to-date and updated procedures are not available on Slack, consult with the Payload Software team.
If the Payload Software team is not available to be consulted, utilize `master`.

`git checkout master`

`git checkout dev`

Open the config.json file in payload-software/main_system/components/config.json to modify the control and imaging params.

To run the MSS with the live sensor data streams, run:

`python ./wrapper_live.py`

Alternatively, to run the MSS in a simulated environment using historical or expected flight data, run:

`python ./wrapper_sim.py`
