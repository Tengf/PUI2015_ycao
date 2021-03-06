import json
import sys
import urllib2
import csv

if __name__ == '__main__':
    url = "http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s" % (
        sys.argv[1], sys.argv[2])
    request = urllib2.urlopen(url)
    mtadata = json.load(request)

    VehicleActivity = mtadata['Siri']['ServiceDelivery'][
        'VehicleMonitoringDelivery'][0]['VehicleActivity']
    num_bus = len(VehicleActivity)

    with open(sys.argv[3], 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Latitude', 'Longitude', 'Stop Name', 'Stop Status'])
        for i in range(0, num_bus):
            Lat = VehicleActivity[i]['MonitoredVehicleJourney'][
                'VehicleLocation']['Latitude']
            Lon = VehicleActivity[i]['MonitoredVehicleJourney'][
                'VehicleLocation']['Longitude']
            if VehicleActivity[i]['MonitoredVehicleJourney']['OnwardCalls'] == {}:
                Stop_Name = 'N/A'
                Stop_Status = 'N/A'
            else:
                Stop_Name = VehicleActivity[i]['MonitoredVehicleJourney'][
                    'OnwardCalls']['OnwardCall'][0]['StopPointName']
                Stop_Status = VehicleActivity[i]['MonitoredVehicleJourney']['OnwardCalls'][
                    'OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']
            writer.writerow([Lat, Lon, Stop_Name, Stop_Status])
