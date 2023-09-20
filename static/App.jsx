function App() {
  const [playerSearch, setPlayerSearch] = React.useState("");
  const [playerData, setPlayerData] = React.useState({});
  const [rankedData, setRankedData] = React.useState({});
  const [searchStatus, setSearchStatus] = React.useState();

  /* Function to fetch basic player data */
  function searchForPlayer() {
    const PROXY_URL = "/api/proxy?url=https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + playerSearch;

  function sendPlayerData(playerData) {
    const playerDetailsURL = '/player_details';
        const pData = {
          puuid: playerData.puuid,
          summonerLevel: playerData.summonerLevel,
          name: playerData.name 
         };
         console.log(pData)
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
        // could make another api call, now that you have the puuid
        sendPlayerData(data);
      })
      .catch((error) => {
        console.error('Fetch error:', error);
        setSearchStatus('Player Not Found');
      });
  }
  /* Use useEffect to fetch ranked data after the initial render, had problems before using useEffect. */
  React.useEffect(() => {
    if (playerData.id) {
      const PROXY_URL = "/api/proxy?url=https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + playerData.id;

      fetch(PROXY_URL)
        .then((response) => response.json())
        .then(data => {
          console.log(data);
          setRankedData(data);
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
    }
  }, [playerData.id]); // ensure the effect runs when playerData.id changes to prevent re-render issues

  return (
    <div className="PlayerSearch">
      <div className="container">
        <h1>Teamfight Tactics Player Search</h1>
        <input type="text" onChange={e => setPlayerSearch(e.target.value)}></input>
        <button onClick={searchForPlayer}>View Player</button>
      </div>
      {searchStatus === 'Player Found' ? (
        <React.Fragment>
          <p>Player Found!</p>
          {playerData && (
            <React.Fragment>
              <p>Summoner level {playerData.summonerLevel}</p>
              <img
                width="100"
                height="100"
                src={
                  'http://ddragon.leagueoflegends.com/cdn/13.17.1/img/profileicon/' +
                  playerData.profileIconId +
                  '.png'
                }
              ></img>
            </React.Fragment>
          )}
          {rankedData.length > 0 ? (
            <p>
              Rank: {rankedData[0].tier} {rankedData[0].rank}
            </p>
          ) : (
            <p>This player is unranked.</p>
          )}
        </React.Fragment>
      ) : searchStatus === 'Player Not Found' ? (
        <p>Player Not Found!</p>
      ) : null}
    </div>
  );
}

ReactDOM.render(<App />, document.querySelector('#root'));
