using System;
using FSUIPC;
using System.IO;

class Program
{
    // Define the path where the screenshot will be saved
    static string screenshotDirectory = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyPictures), "GeoShottr");

    static void Main()
    {
        // Try to open the FSUIPC connection
        try
        {
            FSUIPCConnection.Open();
            Console.WriteLine("FSUIPC Connected!");

            // Read the current latitude and longitude from FSUIPC offsets
            uint latLow = 0, latHigh = 0;
            uint lonLow = 0, lonHigh = 0;

            // Read Latitude and Longitude from their respective offsets
            latLow = (uint)FSUIPCConnection.ReadLVar("LatitudeLow");
            latHigh = (uint)FSUIPCConnection.ReadLVar("LatitudeHigh");
            lonLow = (uint)FSUIPCConnection.ReadLVar("LongitudeLow");
            lonHigh = (uint)FSUIPCConnection.ReadLVar("LongitudeHigh");

            // Convert the high and low parts into the correct latitude and longitude
            double latitude = ConvertFSUIPCToDegrees(latHigh, latLow, 90.0, 10001750.0);
            double longitude = ConvertFSUIPCToDegrees(lonHigh, lonLow, 360.0, 65536.0);

            // Output the latitude and longitude from FSUIPC
            Console.WriteLine($"Latitude: {latitude:F6}, Longitude: {longitude:F6}");

            // Close the connection to FSUIPC
            FSUIPCConnection.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"FSUIPC connection failed: {ex.Message}. Ensure FSUIPC is running.");
        }
    }

    // Convert the FSUIPC data to decimal degrees
    static double ConvertFSUIPCToDegrees(uint highPart, uint lowPart, double factor, double divisor)
    {
        // Convert the high and low parts into one double
        double high = (double)highPart;
        double low = (double)lowPart / (65536.0 * 65536.0);

        // Combine the parts
        double result = high + low;

        // Scale to degrees
        result = result * factor / divisor;

        return result;
    }
}
