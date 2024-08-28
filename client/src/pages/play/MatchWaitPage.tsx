import React from "react";

interface MatchWaitPagePorps {
  handleCancel: () => void;
}

const MatchWaitPage: React.FC<MatchWaitPagePorps> = ({ handleCancel }) => {
  return (
    <div>
      <div>matching...</div>
      <button onClick={handleCancel}>cancel</button>
    </div>
  );
};

export default MatchWaitPage;
