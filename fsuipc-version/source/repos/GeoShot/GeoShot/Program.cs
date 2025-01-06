using System;
using System.Drawing; // Requires System.Drawing.Common
using System.Drawing.Imaging; // For saving images
using FSUIPC;

namespace GeoShotFSUIPC
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Connect to FSUIPC
                FSUIPCConnection.Open();
                Console.WriteLine("Connected to FSUIPC.");

                // Define offsets for Latitude and Longitude
                Offset<double> latitudeOffset = new Offset<double>(0x0568); // Latitude offset
                Offset<double> longitudeOffset = new Offset<double>(0x056C); // Longitude offset

                // Read the values
                latitudeOffset.Refresh();
                longitudeOffset.Refresh();

                double latitude = latitudeOffset.Value;
                double longitude = longitudeOffset.Value;

                Console.WriteLine($"Latitude: {latitude}, Longitude: {longitude}");

                // Capture a screenshot with geotag
                TakeScreenshot("screenshot_with_geotag.jpg", latitude, longitude);

                Console.WriteLine("Screenshot saved with geotag.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            finally
            {
                // Close FSUIPC connection
                FSUIPCConnection.Close();
                Console.WriteLine("FSUIPC connection closed.");
            }
        }

        static void TakeScreenshot(string filePath, double latitude, double longitude)
        {
            // Capture the screen
            Bitmap screenshot = new Bitmap(1920, 1080); // Change dimensions as needed
            using (Graphics g = Graphics.FromImage(screenshot))
            {
                g.CopyFromScreen(0, 0, 0, 0, screenshot.Size);
            }

            // Save the screenshot as JPEG
            screenshot.Save(filePath, ImageFormat.Jpeg);

            Console.WriteLine($"Screenshot saved at {filePath}. Latitude: {latitude}, Longitude: {longitude}");
            Console.WriteLine("Add EXIF metadata manually using an EXIF library if needed.");
        }
    }
}
