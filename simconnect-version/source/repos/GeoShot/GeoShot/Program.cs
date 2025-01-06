using System;
using Microsoft.FlightSimulator.SimConnect;
using System.Runtime.InteropServices;  // For Marshal

namespace GeoShot
{
    public class GeoShotApp
    {
        // Define the Position structure to hold lat/lon data
        [StructLayout(LayoutKind.Sequential)]
        public struct Position
        {
            public double Latitude;
            public double Longitude;
        }

        // Enum to identify data request types
        public enum Definitions
        {
            Position
        }

        // Enum to identify requests
        public enum Requests
        {
            Position
        }

        // Declare the SimConnect object
        private static SimConnect? simconnect = null;

        // Event handler for receiving SimConnect data
        private static void OnRecvSimobjectData(SimConnect sender, SIMCONNECT_RECV_SIMOBJECT_DATA data)
        {
            if (data.dwRequestID == (uint)Requests.Position)
            {
                // Validate that the dwData array is non-null and has elements
                if (data.dwData != null && data.dwData.Length > 0)
                {
                    try
                    {
                        // Ensure the first element is not null before unboxing
                        if (data.dwData[0] != null)
                        {
                            // Marshal the raw data into the Position struct (latitude and longitude)
                            GCHandle handle = GCHandle.Alloc(data.dwData[0], GCHandleType.Pinned);
                            try
                            {
                                Position position = (Position)Marshal.PtrToStructure(handle.AddrOfPinnedObject(), typeof(Position));

                                // Validate and output the position data
                                if (double.IsNaN(position.Latitude) || double.IsNaN(position.Longitude) ||
                                    position.Longitude < -180 || position.Longitude > 180 ||
                                    position.Latitude < -90 || position.Latitude > 90)
                                {
                                    Console.WriteLine("Received invalid data: Latitude: " + position.Latitude + ", Longitude: " + position.Longitude);
                                }
                                else
                                {
                                    // Print valid position data
                                    Console.WriteLine($"Lat: {position.Latitude}, Lon: {position.Longitude}");
                                }
                            }
                            finally
                            {
                                handle.Free();
                            }
                        }
                        else
                        {
                            Console.WriteLine("Error: Data element is null.");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("Error marshalling position data: " + ex.Message);
                    }
                }
                else
                {
                    Console.WriteLine("Error: Invalid data buffer (dwData is null or empty).");
                }
            }
        }



        // Initialize the SimConnect connection
        private static void InitializeSimConnect()
        {
            try
            {
                // Connect to the simulator
                simconnect = new SimConnect("GeoShot", IntPtr.Zero, 0, null, 0);

                // Register the event handler for receiving data
                simconnect.OnRecvSimobjectData += OnRecvSimobjectData;

                // Add data definitions for position (latitude and longitude)
                simconnect.AddToDataDefinition(
                    (Enum)Definitions.Position,            // Corrected: Cast the enum to Enum type
                    "PLANE LATITUDE", "degrees",
                    SIMCONNECT_DATATYPE.FLOAT64,
                    0.001f, 0);
                simconnect.AddToDataDefinition(
                    (Enum)Definitions.Position,            // Corrected: Cast the enum to Enum type
                    "PLANE LONGITUDE", "degrees",
                    SIMCONNECT_DATATYPE.FLOAT64,
                    0.001f, 0);

                // Request position data every second for the user aircraft
                simconnect.RequestDataOnSimObject(
                    (Enum)Requests.Position,              // Corrected: Cast the enum to Enum type
                    (Enum)Definitions.Position,          // Corrected: Cast the enum to Enum type
                    SimConnect.SIMCONNECT_OBJECT_ID_USER, // User aircraft
                    SIMCONNECT_PERIOD.SECOND,             // Request data every second
                    SIMCONNECT_DATA_REQUEST_FLAG.DEFAULT, // Use default flags
                    0, 0, 0                               // Additional parameters (not needed here)
                );

                Console.WriteLine("Listening for position data...");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error initializing SimConnect: " + ex.Message);
            }
        }

        // Main method to start the application
        static void Main(string[] args)
        {
            // Initialize SimConnect
            InitializeSimConnect();

            // Keep the application running to receive data
            while (true)
            {
                // Process any SimConnect events (data requests)
                simconnect?.ReceiveMessage();
            }
        }
    }
}
