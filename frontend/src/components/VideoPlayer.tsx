import React from 'react';
import ReactPlayer from 'react-player';

interface VideoPlayerProps {
  url: string;
  width?: string;
  height?: string;
  controls?: boolean;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({
  url,
  width = "100%",
  height = "100%",
  controls = true,
}) => {
  return (
    <div className="video-player">
      <ReactPlayer url={url} width={width} height={height} controls={controls} />
    </div>
  );
};

export default VideoPlayer;
