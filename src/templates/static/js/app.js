
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');



    const socket = io.connect(); // sends initial socket connection to py server


    socket.on('init', (data) => {
        console.log('connected to server');
        console.log(BSON.deserialize(data));
    });

    socket.on('update', (data) => {
        console.log('update recieved');
        console.log(BSON.deserialize(data));
        }
    )


    socket.on('disconnect', () => {
        console.log('Disconnected from the server');
    });




        // Add event listener for beforeunload event
    window.addEventListener('beforeunload', () => {
                socket.disconnect();
            });

       // window.addEventListener('resize', updateView);
    });