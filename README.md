# RF-Switcher-Website
Provides an Website to control 433 mhz radio controlled sockets using only flask.
Uses [433Utils/RPi_utils](https://github.com/ninjablocks/433Utils/tree/master/RPi_utils) codesend.

## Example
![Website](https://github.com/JDEVDAIN/RF-Switcher-Website/blob/master/Website.PNG?raw=true)


## Home Assistant Configuration Example
Can be added as a [RESTful Switch](https://www.home-assistant.io/integrations/switch.rest/) in Home Assistant. 
```
switch:                                                                                                                                                              
- platform: rest                                                                                                                                                     
  name: "LED Desk"                                                                                                                                           
  resource: http://<Endpoint>/api/switches                                                                                                                   
  body_on: '{"name": "1", "value": "ON"}'                                                                                                                            
  body_off: '{"name": "1", "value": "OFF"}'                                                                                                                          
  headers:                                                                                                                                                           
      Content-Type: application/json                                                                                                                                 
  state_resource: http://<Endpoint>/api/status/1                                                                                                             
  is_on_template: '{{ value_json.status }}'                                                                                                                          
                                                                                                                                                                     
- platform: rest                                                                                                                                                     
  name: "Lamp"                                                                                                                                                   
  resource: http://<Endpoint>/api/switches                                                                                                                   
  body_on: '{"name": "2", "value": "ON"}'                                                                                                                            
  body_off: '{"name": "2", "value": "OFF"}'                                                                                                                          
  headers:                                                                                                                                                           
      Content-Type: application/json                                                                                                                                 
  state_resource: http://<Endpoint>/api/status/2                                                                                                             
  is_on_template: '{{ value_json.status}}'  
```
