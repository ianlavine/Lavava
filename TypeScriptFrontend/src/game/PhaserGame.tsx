import React, {
    forwardRef,
    useEffect,
    useLayoutEffect,
    useRef,
    useContext,
    useState,
} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import StartGame from "./main";
import { EventBus } from "./EventBus";
import { NetworkContext } from "./NetworkContext";
import { Network } from "./objects/network";
import { useBlocker } from "react-router-dom";
export interface IRefPhaserGame {
    game: Phaser.Game | null;
    scene: Phaser.Scene | null;
}

interface IProps {
    currentActiveScene?: (scene_instance: Phaser.Scene) => void;
    props?: any;
    network?: Network | null;
}

export const PhaserGame = forwardRef<IRefPhaserGame, IProps>(
    function PhaserGame({ currentActiveScene }, ref) {
        const network = useContext(NetworkContext);
        const navigate = useNavigate();
        const game = useRef<Phaser.Game | null>(null!);
        const location = useLocation();
        const boardData = location.state?.boardData;
        const [dirty, setDirty] = useState(true);
        let blocker = useBlocker(
            ({ currentLocation, nextLocation }) =>
                nextLocation == null || nextLocation.pathname === "/lobby"
        );
        console.log("location: ", boardData);
        console.log("blocker: ", blocker);

        useLayoutEffect(() => {
            if (game.current === null) {
                game.current = StartGame(
                    "game-container",
                    boardData,
                    network as Network,
                    navigate
                );

                if (typeof ref === "function") {
                    ref({ game: game.current, scene: null });
                } else if (ref) {
                    ref.current = { game: game.current, scene: null };
                }
            }

            return () => {
                if (game.current) {
                    game.current.destroy(true);
                    if (game.current !== null) {
                        game.current = null;
                    }
                }
            };
        }, [ref, boardData]);

        useEffect(() => {
            EventBus.on(
                "current-scene-ready",
                (scene_instance: Phaser.Scene) => {
                    if (
                        currentActiveScene &&
                        typeof currentActiveScene === "function"
                    ) {
                        currentActiveScene(scene_instance);
                    }

                    if (typeof ref === "function") {
                        ref({ game: game.current, scene: scene_instance });
                    } else if (ref) {
                        ref.current = {
                            game: game.current,
                            scene: scene_instance,
                        };
                    }
                }
            );
            return () => {
                EventBus.removeListener("current-scene-ready");
            };
        }, [currentActiveScene, ref]);
        return (
            <div>
                {/* {blocker.state === "blocked" ? (
                    <div>
                        <p>Are you sure you want to leave?</p>
                        <button onClick={() => blocker.proceed()}>
                            Proceed
                        </button>
                        <button onClick={() => blocker.reset()}>Cancel</button>
                    </div>
                ) : null} */}
                <div id="game-container"></div>{" "}
            </div>
        );
    }
);

