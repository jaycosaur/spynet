import React from "react";

interface INodeInformation {
  nodeId: string;
  isOnline: boolean;
}

export const VideoView: React.FC = () => {
  const [cameraId, setCameraId] = React.useState("");
  const [availableCameras, setAvailableCameras] = React.useState<
    INodeInformation[]
  >([]);

  React.useEffect(() => {
    fetch("http://localhost:5000/nodes")
      .then(res => res.json())
      .then(json => {
        if (Array.isArray(json)) {
          const nodeInfo = json as INodeInformation[];
          setAvailableCameras(nodeInfo);
          if (nodeInfo.length > 0) {
            setCameraId(nodeInfo[0].nodeId);
          }
        }
      });
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      <div style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        {availableCameras.map(cam => (
          <div
            key={cam.nodeId}
            style={{
              margin: 8,
              padding: 32,
              border: "1px solid black",
              borderRadius: 8,
              display: "flex",
              flexDirection: "column",
              flex: 1,
              justifyContent: "center",
              alignItems: "center"
            }}
            onClick={() => setCameraId(cam.nodeId)}
          >
            <span>
              {cam.nodeId} | ONLINE {cam.isOnline ? "Yes" : "No"}
            </span>
            <VideoPlayer cameraId={cam.nodeId} width={250} />
          </div>
        ))}
      </div>
      <VideoPlayer cameraId={cameraId} width={1400} />
    </div>
  );
};

export const VideoPlayer: React.FC<{
  cameraId: string;
  width: number;
}> = props => {
  return (
    <img
      key={props.cameraId}
      src={`http://localhost:5000/nodes/${props.cameraId}/video_feed`}
      width={props.width}
    />
  );
};
