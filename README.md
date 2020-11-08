# Chirpstack_lora_cloud_project
Linux based project which uses the python framework Dash to display data in web format.
The project is using the LoRaWAN-Chirpstack stack as follows: 

![alt text](https://github.com/JacobKjaerager/Chirpstack_lora_cloud_project/blob/main/non_code_graphics/Architecture_lora_project.PNG?raw=true)

The project uses the Postgres integration from the Chirpstack-application-server to update 3 preconfigured tables device_up, device_join and device_status.
The Flask-based Dash application is configured to make time-based requests to the device_up table every 60 seconds. 
This is a demonstation to what could be made for each individual application. 
As the payload is different pr. application, the decoding is difficult to make fully dynamic in one SPA. 
For future development general application based on CayenneLPP payload, can be made for fully dynamic plug and play application.

This result in the Web application is seen below as pr. 08-11-2020
![alt text](https://github.com/JacobKjaerager/Chirpstack_lora_cloud_project/blob/main/non_code_graphics/Web_view.PNG?raw=true)
