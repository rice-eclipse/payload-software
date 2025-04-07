

function Payload_Analysis
% Graphing data collected during rPAYLOAD's maiden flight

hib_table = readtable("data_logs/hib_sensor_log.csv");

launchtime = 123440;

hold on
subplot(4,1,1)
plot(hib_table{launchtime:end,1}, hib_table{launchtime:end,2})
title("Altitude vs Time")
ylabel("Altitude (ft)")
subplot(4,1,2)
plot(hib_table{launchtime:end,1}, hib_table{launchtime:end,3})
title("Angle vs Time")
ylabel("Angle (rad)")
subplot(4,1,3)
plot(hib_table{launchtime:end,1}, hib_table{launchtime:end,4})
title("Acceleration vs Time")
ylabel("Proper Acceleration (ft/s^2)")
subplot(4,1,4)
hold on
plot(hib_table{launchtime:end,1}, hib_table{launchtime:end,14})
plot(hib_table{launchtime:end,1}, hib_table{launchtime:end,15})
legend("Payload Temp", "Core Temp")
title("Temperature vs Time")
ylabel("Temperature (deg C)")
% legend("Altitude", "Angle", "Acceleration", "Payload temp", "Core temp")
xlabel("Time (milliseconds since power on)")
end

