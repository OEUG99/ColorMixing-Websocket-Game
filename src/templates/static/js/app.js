document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');


            const socket = io.connect();

            socket.on('connect', () => {
                console.log('Connected to the server');
            });

            socket.on('disconnect', () => {
                console.log('Disconnected from the server');
            });

            function drawGrid(ctx, gridSize) {
                width = 10000;
                height = 10000;

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;

                for (let x = -width; x <= width; x += gridSize) {
                    ctx.beginPath();
                    ctx.moveTo(x, -height);
                    ctx.lineTo(x, height);
                    ctx.stroke();
                }

                for (let y = -height; y <= height; y += gridSize) {
                    ctx.beginPath();
                    ctx.moveTo(-width, y);
                    ctx.lineTo(width, y);
                    ctx.stroke();
                }
            }


    function updateView(data, ctx, canvas, socket) {
        console.log('game view updated');
        console.log(data);

        // resize canvas
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Find the current player using socket.id
        const currentPlayer = data.players.find(player => player.id === socket.id);
        if (!currentPlayer) {
            return;
        }

        // Clear the canvas
        ctx.fillStyle = "#505050"; // set the default colour
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Apply the camera translation
        ctx.save();

        // Calculate the scale factor based on player size
        const baseScale = 1.0; // Initial scale of the camera
        const sizeFactor = 100; // Controls how quickly camera zooms out
        const scaleFactor = baseScale / (1 + currentPlayer.size / sizeFactor);

        // Set the transformation origin to the center of the canvas
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        ctx.translate(centerX, centerY);

        // Apply the scale transformation
        ctx.scale(scaleFactor, scaleFactor);

        // Move the transformation origin back to the top-left corner
        ctx.translate(-centerX, -centerY);

        // Calculate the camera translation
        const translateX = centerX - currentPlayer.x;
        const translateY = centerY - currentPlayer.y;
        ctx.translate(translateX, translateY);

        // Draw grid background
        drawGrid(ctx, 50);

        // Calculate the maximum distance for rendering objects
        const maxRenderDistance = Math.sqrt(canvas.width * canvas.width + canvas.height * canvas.height) / 2;

        // Render the players
        for (const player of data.players) {
            const distance = Math.sqrt(Math.pow(currentPlayer.x - player.x, 2) + Math.pow(currentPlayer.y - player.y, 2));
            if (distance <= maxRenderDistance) {
                ctx.beginPath();
                ctx.arc(player.x, player.y, player.size, 0, 2 * Math.PI);
                ctx.fillStyle = player.color;
                console.log(player.color)
                ctx.fill();
                ctx.closePath();
            }
        }

        function drawStar(ctx, cx, cy, spikes, outerRadius, innerRadius, color) {
            let rot = (Math.PI / 2) * 3;
            let x = cx
            let y = cy ;
            const step = Math.PI / spikes;

            ctx.beginPath();
            ctx.moveTo(cx, cy - outerRadius);

            for (let i = 0; i < spikes; i++) {
                x = cx + Math.cos(rot) * outerRadius;
                y = cy + Math.sin(rot) * outerRadius;
                ctx.lineTo(x, y);
                rot += step;

                x = cx + Math.cos(rot) * innerRadius;
                y = cy + Math.sin(rot) * innerRadius;
                ctx.lineTo(x, y);
                rot += step;
            }

            ctx.lineTo(cx, cy - outerRadius);
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        }

        // render entities
        for (const entity of data.entities) {
            const distance = Math.sqrt(Math.pow(currentPlayer.x - entity.x, 2) + Math.pow(currentPlayer.y - entity.y, 2));
            if (distance <= maxRenderDistance) {
                // Replace the arc drawing with a call to the drawStar function
                drawStar(ctx, entity.x, entity.y, 5, entity.size*2, entity.size / 4, entity.color);
                console.log(entity.color);
            }
        }

        // Reset the camera translation
        ctx.restore();
    }


            socket.on('update', (data) => {
                updateView(data, ctx, canvas, socket);
            });


        // Add event listener for arrow key movements
        window.addEventListener('keydown', (event) => {
                // Determine which arrow key was pressed and store as string
                  let movementKey;
                    if (event.key === 'ArrowUp')
                        movementKey = 'up';
                    else if (event.key === 'ArrowDown')
                        movementKey = 'down';
                    else if (event.key === 'ArrowLeft')
                        movementKey = 'left';
                    else if (event.key === 'ArrowRight')
                        movementKey = 'right';
                    else if (event.key === "Spacebar" || event.key === " ")
                        movementKey = "space"

                // Send the movement action to the server
                socket.emit('player_arrow_movement', movementKey);
            });



        // Add event listener for beforeunload event
        window.addEventListener('beforeunload', () => {
                socket.disconnect();
            });

            window.addEventListener('resize', updateView);
        });