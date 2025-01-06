using System;
using FSUIPC;
using System.IO;
using System.Threading;

class Program
{
    // Define the path where the screenshot will be saved
    static string screenshotDirectory = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyPictures), "GeoShottr");

    static void Main()
    {
        // Ensure the screenshot directory exists
        Directory.CreateDirectory(screenshotDirectory);

        // Try to open the FSUIPC connection
        try
        {
            FSUIPCConnection.Open();
            Console.WriteLine("FSUIPC Connected!");

            while (true)  // Continuous polling loop
            {
                // Read Latitude and Longitude using their actual numeric offsets (0x0560 for low part, 0x0564 for high part for Latitude)
                uint latLow = (uint)FSUIPCConnection.ReadLVar("L:LatitudeLow"); // Latitude Low (32-bit)
                uint latHigh = (uint)FSUIPCConnection.ReadLVar("L:LatitudeHigh"); // Latitude High (32-bit)
                uint lonLow = (uint)FSUIPCConnection.ReadLVar("L:LongitudeLow"); // Longitude Low (32-bit)
                uint lonHigh = (uint)FSUIPCConnection.ReadLVar("L:LongitudeHigh"); // Longitude High (32-bit)

                // Convert the high and low parts into the correct latitude and longitude
                double latitude = ConvertFSUIPCToDegrees(latHigh, latLow, 90.0, 10001750.0);
                double longitude = ConvertFSUIPCToDegrees(lonHigh, lonLow, 360.0, 65536.0);

                // Output the latitude and longitude from FSUIPC
                Console.WriteLine($"Latitude: {latitude:F6}, Longitude: {longitude:F6}");

                // Sleep for 1 second before polling again
                Thread.Sleep(1000);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"FSUIPC connection failed: {ex.Message}. Ensure FSUIPC is running.");
        }
        finally
        {
            // Close the connection to FSUIPC
            FSUIPCConnection.Close();
        }
    }

    // Convert the FSUIPC data to decimal degrees
    static double ConvertFSUIPCToDegrees(uint highPart, uint lowPart, double factor, double divisor)
    {
        // Convert the high and low parts into one double
        double high = (double)highPart;
        double low = (double)lowPart / (65536.0 * 65536.0); // Correct the scale of the low part

        // Combine the parts
        double result = high + low;

        // Scale to degrees
        result = result * factor / divisor;

        return result;
    }
}
