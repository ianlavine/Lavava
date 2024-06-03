import { Node } from "./node";
// import { State } from "./States";
import { Edge } from "./edge";
import { OtherPlayer } from "./otherPlayer";
import { MyPlayer } from "./myPlayer";
// import { ClickType } from "../enums";
import { PlayerColors, PORT_COUNT } from "../constants";
import { stateDict } from "./States";
import { random_equal_distributed_angles } from "../utilities";
// import * as Phaser from "phaser";
import { Scene } from "phaser";

// const Phaserr = require("phaser");

type NodeData = {
    effects: any[]; // Replace `any` with a more specific type if possible
    is_port: boolean;
    pos: [number, number];
    state: number;
    value: number;
};

type EdgeData = {
    dynamic: boolean;
    from_node: number;
    to_node: number;
};

type AbilityValue = {
    credits: number;
    reload: number;
};

type AbilitiesData = {
    values: { [key: string]: AbilityValue };
    credits: number;
};

type BoardData = {
    board: {
        nodes: { [id: string]: NodeData };
        edges: { [id: string]: EdgeData };
    };
    player_count: number;
    player_id: number;
    abilities: AbilitiesData;
};

export class Main {
    // ps: string;
    // timer: number;
    // highlight: Highlight;
    // effectVisuals: { [key: string]: any } = {};
    // canDraw: boolean = false;
    myPlayer: any;
    players: { [key: string]: any };
    nodes: { [key: string]: any };
    edges: { [key: string]: any };

    constructor() {}

    settings(): [any, number] {
        // Placeholder: replace with actual settings retrieval logic
        return [{}, 8080];
    }

    setup(startData: BoardData): void {
        if (
            startData &&
            startData.board &&
            startData.board.nodes &&
            startData.board.edges &&
            startData.player_count &&
            startData.player_id &&
            startData.abilities
        ) {
            console.log("hereadsad");
            const pi = Number(startData.player_id.toString());
            const pc = startData.player_count;
            const n = startData.board.nodes;
            const e = startData.board.edges;
            // const abi = startData.abilities.values;
            // const credits = startData.abilities.credits;

            this.myPlayer = new MyPlayer(String(pi), PlayerColors[pi]);
            this.players = Object.fromEntries(
                Object.keys([...Array(pc).keys()].filter((id) => id != pi)).map(
                    (id) => [
                        id,
                        new OtherPlayer(
                            id.toString(),
                            PlayerColors[Number(id)]
                        ),
                    ]
                )
            );
            const scene = new Scene();
            this.players[pi] = this.myPlayer;
            this.nodes = Object.fromEntries(
                Object.keys(n).map((id) => [
                    id,
                    new Node(
                        Number(id),
                        n[id]["pos"],
                        n[id]["is_port"],
                        0.0, // Placeholder: replace with actual value of portPercent
                        n[id]["is_port"]
                            ? random_equal_distributed_angles(PORT_COUNT)
                            : [],
                        stateDict[n[id]["state"]],
                        n[id]["value"]
                        // scene
                    ),
                ])
            );
            this.edges = Object.fromEntries(
                Object.keys(e).map((id) => [
                    id,
                    new Edge(
                        // scene,
                        Number(id),
                        this.nodes[e[id]["from_node"]],
                        this.nodes[e[id]["to_node"]],
                        e[id]["dynamic"]
                    ),
                ])
            );
            console.log("num edges: ", Object.keys(this.nodes).length);
        } else {
            console.log("not here");
        }
    }
    getObject(object, attribute, value) {
        if (object[attribute] instanceof Node) {
            return this.nodes[value];
        } else if (object[attribute] instanceof Edge) {
            return this.edges[value];
        }
        //TODO: check for State and OtherPlayer types after adding those
        else {
            return value;
        }
    }
    parse(items, updates) {
        if (!items || typeof items !== "object" || Array.isArray(items)) {
            throw new Error("Invalid 'items' parameter; expected an object.");
        }
        if (!updates || typeof updates !== "object" || Array.isArray(updates)) {
            throw new Error("Invalid 'updates' parameter; expected an object.");
        }

        for (const u in updates) {
            if (!items.hasOwnProperty(u)) {
                console.error(`No item found for key ${u}`);
                continue;
            }

            let obj = items[u];
            if (typeof obj !== "object" || obj === null) {
                console.error(`Invalid item at key ${u}; expected an object.`);
                continue;
            }

            for (const [key, val] of Object.entries(updates[u])) {
                if (typeof obj[key] === "undefined") {
                    console.error(`Key ${key} not found in item ${u}.`);
                    continue;
                }

                console.log("before: " + obj[key]);
                let updateVal;
                try {
                    updateVal = this.getObject(obj, key, val);
                } catch (error) {
                    console.error(
                        `Error updating key ${key} in item ${u}: ${error.message}`
                    );
                    continue;
                }

                obj[key] = updateVal;
                console.log("updated key: ", key, " with value: ", val);
                console.log("after: " + obj[key]);
            }
        }
    }
}

