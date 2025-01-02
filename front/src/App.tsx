import { useState } from 'react'
import './App.css'
import "bootstrap/dist/css/bootstrap.min.css";

console.log(process.env);
const API_URL = process.env.API_URL || "http://localhost:31331";

function App() {
  const [musicName, setMusicName] = useState<string>("");
  const [musicList, setMusicList] = useState<string[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [modalBody, setModalBody] = useState<string>("");
  const [version, setVersion] = useState<string | null>("0.0.0");
  const [modelDate, setModelDate] = useState<string | null>("01/01/1960");


  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const chunkArray = (array: string[], chunkSize: number) => {
    const result: string[][] = [];
    for (let i = 0; i < array.length; i += chunkSize) {
      result.push(array.slice(i, i + chunkSize));
    }
    return result;
  };

  const handleAddMusic = () => {
    if (musicName.trim()) {
      setMusicList([...musicList, musicName.trim()]);
      console.log(musicList);
      setMusicName("");
    }
  };

  const handleDiscoverRecommendations = async () => {
    try {
      const response = await fetch(`${API_URL}/api/recomend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ musicList }),
      });
      
      const data = await response.json();
      setModalBody(data.songs);
      setVersion(data.version);
      setModelDate(data.model_date);
      handleOpenModal();
    } catch (error) {
      setModalBody(`Erro ao enviar requisição: ${error}`);
      handleOpenModal();
    }
  };

  return (
    <>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Suas Músicas"
          aria-label="Suas Músicas"
          aria-describedby="btn-add"
          value={musicName}
          onChange={(e) => setMusicName(e.target.value)}
        />
        <button className="btn btn-outline-secondary" type="button" id="btn-add" onClick={handleAddMusic}>
          Adicionar
        </button>
      </div>
      <div>
        {chunkArray(musicList, 3).map((chunk, chunkIndex) => (
          <ul key={chunkIndex} className="list-group list-group-horizontal">
            {chunk.map((music, index) => (
              <li key={index} className="list-group-item">
                {music}
              </li>
            ))}
          </ul>
        ))}
      </div>
      <button className="btn btn-primary btn-lg mt-2" type="button" id="button-send" onClick={handleDiscoverRecommendations}>
        Descobrir Recomendações
      </button>

      {showModal && (
        <div className="modal show" tabIndex={-1} style={{ display: "block" }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Recomendações</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={handleCloseModal}
                  aria-label="Close"
                ></button>
              </div>
              <div className="modal-body">
                <p>{modalBody}</p>
              </div>
              <div className="modal-footer d-flex justify-content-between">
                <div className='text-start'>
                  <div>
                    Version: <span>{version}</span>
                  </div>
                  <div>
                    Model Date: <span>{modelDate}</span>
                  </div>
                </div>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleCloseModal}
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default App
