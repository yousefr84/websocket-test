import {useState, useRef, useEffect} from 'react';
import axios from "../axios";
import {AxiosError} from "axios";
import type {WebsocketUrlTypes} from "../types";

export function Websocket() {
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [websocketInfo, setWebsocketInfo] = useState<WebsocketUrlTypes>({
    group_name: "",
    message: "",
    websocket_url: ""
  });
  const socketRef = useRef<WebSocket | null>(null);

  const token: string | null = sessionStorage.getItem("token");

  useEffect(() => {
    connectWebsocket()
  } , [websocketInfo]);

  async function startChat() {
    axios.post("start-chat/", {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then((response): void => {
      setWebsocketInfo(response.data);

    }).catch((error: unknown) => {
      const err = error as AxiosError;

      if (err.response?.data) {
        const data = err.response.data as { message?: string };
        setError(data.message || "start chat failed");
      } else {
        setError(err.message || "start chat failed");
      }
    });
  }

  function connectWebsocket(): void {
    const ws = new WebSocket(websocketInfo.websocket_url);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setError(null);
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      setMessage(response.message);
      console.log('WebSocket onMessage');
    };

    ws.onerror = (event) => {
      console.error('WebSocket error:', event);
      setError('WebSocket connection error');
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    socketRef.current = ws;
  }

  async function sendMessage(): Promise<void> {
    await axios.get("send-test-message/", {
      params: {
        group_name: websocketInfo.group_name,
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
  }

  return (
    <div className="text-gray-300 text-center">
      <h1>WebSocket</h1>

      {message && (
        <h1 className="text-green-500 mt-4">Message: {message}</h1>
      )}

      <div>
        <button
          className="border-2 rounded-xl px-3 py-1 cursor-pointer mt-10"
          onClick={startChat}
        >
          Click To Make WebSocket Connection
        </button>
      </div>

      <div className={'mt-10'}>
        {
          message &&
            <button
                className="border-2 rounded-xl px-3 py-1 cursor-pointer mt-10" onClick={sendMessage}>send value to
                websocket</button>
        }
      </div>

      {error && <h2 className="text-red-500 mt-10">{error}</h2>}
    </div>
  );
}
