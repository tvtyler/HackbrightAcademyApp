function App() {
  const [playerSearch, setPlayerSearch] = React.useState("");
  const [playerData, setPlayerData] = React.useState({});
  const [rankedData, setRankedData] = React.useState({});
  const [searchStatus, setSearchStatus] = React.useState();

  /* Function to fetch basic player data */
  function searchForPlayer() {
    const PROXY_URL = "/api/proxy?url=https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + playerSearch;

  /* function to send player data such as name and player id to backend */
  function sendPlayerData(playerData) {
    const playerDetailsURL = '/player_details';
        const pData = {
          puuid: playerData.puuid,
          summonerLevel: playerData.summonerLevel,
          name: playerData.name,
          icon: playerData.profileIconId
         };
         console.log(pData);
        fetch(playerDetailsURL, {
            method: 'POST',
            body: JSON.stringify(pData),
            headers: {
                'Content-Type': 'application/json',
            },
        })
          .then((response) => {
              if (response.ok) {
                  console.log('Data sent to the backend');
              } else {
                  console.error('Failed to send puuid');
              }
          })
  }
    fetch(PROXY_URL)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else if (response.status === 404) {
          throw new Error('Player not found');
        } else {
          throw new Error('Server error');
        }
      })
      .then((data) => {
        console.log(data);
        setPlayerData(data);
        setSearchStatus('Player Found');
        sendPlayerData(data);
      })
      .catch((error) => {
        console.error('Fetch error:', error);
        setSearchStatus('Player Not Found');
      });
  }
  /* function to send a players rank to backend */
  function sendRankedData(rankedData) {
    const rankDetailsUrl = "/rank_details";
      const rData = {
        puuid: rankedData[0].puuid,
        rank: rankedData[0].tier
      };
      fetch(rankDetailsUrl, {
        method: 'POST',
        body: JSON.stringify(rData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        if(response.ok) {
          console.log('rank sent')
        } else {
          console.error('failed to send rank')
        }
      })
  }
  /* Use useEffect to fetch ranked data after the initial render. */
  React.useEffect(() => {
    if (playerData.id) {
      const PROXY_URL = "/api/proxy?url=https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + playerData.id;
      
      fetch(PROXY_URL)
        .then((response) => response.json())
        .then(data => {
          console.log(data);
          setRankedData(data);
          sendRankedData(data);
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
    }
    
  }, [playerData.id]); // ensure the effect runs when playerData.id changes to prevent re-render issues

  /* display search form and basic player data  */
  return (
    <div className="PlayerSearch">
      <div className="container" style={{ textAlign: 'center', padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <h1 style={{ fontSize: '24px' }}>Teamfight Tactics Player Search</h1>
        <input
          type="text"
          onChange={(e) => setPlayerSearch(e.target.value)}
          style={{
            width: '100%',
            maxWidth: '300px',
            padding: '10px',
            marginBottom: '10px',
          }}
        />
        <button
          onClick={searchForPlayer}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            cursor: 'pointer',
          }}>
          View Player
        </button>
      </div>
      {searchStatus === 'Player Found' ? (
        <React.Fragment>
          <p style={{ fontSize: '24px', textAlign: 'center' }}><b>Player Found!</b></p>
          {playerData && (
            <React.Fragment>
              <p style={{ fontSize: '24px', textAlign: 'center' }}>Summoner level: {playerData.summonerLevel}</p>
              <div style={{ textAlign: 'center' }}>
                <img
                  width="100"
                  height="100"
                  src={
                    'http://ddragon.leagueoflegends.com/cdn/13.17.1/img/profileicon/' +
                    playerData.profileIconId +
                    '.png'
                  }
                  style={{ borderRadius: '50%', margin: '0 auto' }}
                />
              </div>
            </React.Fragment>
          )}
          {rankedData.length > 0 ? (
            <p style={{ fontSize: '24px', textAlign: 'center' }}>
              Rank: {rankedData[0].tier} {rankedData[0].rank} <br />
              <a href={`/match_history/${playerData.puuid}`} style={{ textDecoration: 'none', color: '#007bff' }}>
                View Match History
              </a>
            </p>
          ) : (
            <p style={{ fontSize: '24px', textAlign: 'center' }}>This player is unranked.</p>
          )}
        </React.Fragment>
      ) : searchStatus === 'Player Not Found' ? (
        <p style={{ fontSize: '24px', textAlign: 'center' }}>Player Not Found!</p>
      ) : null}
    </div>
  );
}

ReactDOM.render(<App />, document.querySelector('#root'));
