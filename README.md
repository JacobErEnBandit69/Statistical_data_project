# Chirpstack_lora_cloud_projectcC
Linux based project which uses the python framework Dash to display data in web format.
The project is using the LoRaWAN-Chirpstack stack as follows: 
![alt text](https://github.com/JacobKjaerager/Chirpstack_lora_cloud_project/blob/main/non_code_graphics/Architecture_lora_project.PDF?raw=true)

The project uses the Postgres integration from the Chirpstack-application-server to update the database, the Flask-based Dash application the makes requests to this pr config every 60 second 

This result in the view seen below pr. 08-11-2020
![alt text](https://github.com/JacobKjaerager/Chirpstack_lora_cloud_project/blob/main/non_code_graphics/Web_view.PNG?raw=true)
