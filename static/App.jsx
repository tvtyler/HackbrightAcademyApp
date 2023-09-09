function App() {
    const [playerSearch, setPlayerSearch] = React.useState("");
    const [playerData, setPlayerData] = React.useState({});
    const [rankedData, setRankedData] = React.useState({});
  
    /* Function to fetch basic player data */
    function searchForPlayer() {
      const PROXY_URL = "/api/proxy?url=https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + playerSearch;
  
      fetch(PROXY_URL)
        .then((response) => response.json())
        .then(data => {
          console.log(data);
          setPlayerData(data);
        })
        .catch(error => {
          console.error('Fetch error:', error);
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
        {JSON.stringify(playerData) !== '{}' ?
          <React.Fragment>
            <p>Player Found!</p>
            <p> Summoner level {playerData.summonerLevel} </p>
            <img width="100" height="100" src={"http://ddragon.leagueoflegends.com/cdn/13.17.1/img/profileicon/" + playerData.profileIconId + ".png"}></img>
            {JSON.stringify(rankedData) !== '{}' ? (
              <p>Rank: {rankedData[0].tier} {rankedData[0].rank}</p>
            ) : (
              <p>Rank data not available.</p>
            )}
          </React.Fragment>
          :
          <p>Player Not Found!</p>
        }
      </div>
    );
  }
  
  ReactDOM.render(<App />, document.querySelector('#root'));
  