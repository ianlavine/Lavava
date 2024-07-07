import { json } from "react-router-dom";
import { NameToCode } from "./constants";

export class Network {
    public socket: WebSocket | null = null;
    serverURL: string;
    updateCallback: (board_data) => void;
    gameIDEtcCallback: (game_id: string, player_count: number) => void;
    messageQueue: Record<any, any> = [];
    private boardDataPromise: Promise<any> | null = null;
    private boardDataResolver: ((data: any) => void) | null = null;
    private reconnectAttempts: number = 0;
    private maxReconnectAttempts: number = 5;
    private reconnectInterval: number = 3000; // 3 seconds
    private token: string | null = "";

    constructor(serverURL: string, updateCallback: () => void) {
        this.serverURL = serverURL;
        this.updateCallback = updateCallback;

        // Initialize the board data promise
        this.boardDataPromise = new Promise((resolve) => {
            this.boardDataResolver = resolve;
        });
    }

    connectWebSocket(): void {
        console.log("Trying to connect to WebSocket...");
        this.socket = new WebSocket(this.serverURL);
        this.token = localStorage.getItem("userToken") || sessionStorage.getItem("guestToken");

        this.socket.onopen = () => {
            console.log("WebSocket Connected");
            this.messageQueue.forEach((msg) => this.sendMessage(msg)); // Send all queued messages
            this.messageQueue = []; // Clear the queue
        };

        this.socket.onmessage = (event) => {
            // console.log("Received message: ", event.data);
            let data = JSON.parse(event.data);
            if (data.hasOwnProperty("game_id")) {
                this.gameIDEtcCallback(data.game_id, data.player_count);
                console.log("Game ID received: ", data.game_id);
            } else {
                if (data.isFirst === true) {
                    // console.log("Board data received");
                    if (this.boardDataResolver) {
                        this.boardDataResolver(data);
                        this.boardDataResolver = null; // Ensure the resolver is called only once
                    }
                } else {
                    // console.log("Calling update callback");
                    this.updateCallback(data);
                }
                // Call the update callback with the received data
            }
        };

        this.socket.onclose = () => {
            console.log("WebSocket Disconnected");

        };

        this.socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };
    }

    attemptReconnect(): void {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(() => this.connectWebSocket(), this.reconnectInterval);
        } else {
            console.error("Max reconnection attempts reached. Please refresh the page.");
        }
    }

    disconnectWebSocket(): void {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
        
        // Reset the board data promise
        this.boardDataPromise = new Promise((resolve) => {
            this.boardDataResolver = resolve;
        });
    
        // Clear the message queue
        this.messageQueue = [];
    }

    sendMessage(message: Record<any, any>): void {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log("Sending message: ", message);
            console.log("Socket: ", this.socket);
            message.token = this.token;
            message.game_id = sessionStorage.getItem("key_code");
            const result = this.socket.send(JSON.stringify(message));
            console.log("Result: ", result);
        } else if (
            this.socket &&
            this.socket.readyState === WebSocket.CONNECTING
        ) {
            console.log("Queuing message due to WebSocket connecting");
            this.messageQueue.push(message);
        } else {
            console.error("WebSocket is not connected or has failed.");
        }
    }

    setupUser(abilities: { [x: string]: any }) {
        console.log("setup called");
        const type = sessionStorage.getItem("type");
        const playerCount = Number(sessionStorage.getItem("player_count")) || 0;

        const send_dict = {
            type: type,
            players: playerCount,
            mode: "default",
            abilities: abilities,
        };
        console.log("Trying to setp user with: ", send_dict);
        this.sendMessage(send_dict);
    }

    // Method to get the board data promise
    getBoardData(): Promise<any> {
        return this.boardDataPromise!;
    }

    test() {
        return "Test called";
    }
}

