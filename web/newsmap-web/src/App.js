import './styles/App.css';
import React, {useState} from 'react';

import region_data from "./regions.json";
import {DEFAULT_START_TIMESTAMP, DEFAULT_END_TIMESTAMP} from "./constants";
import Article from "./components/UI/Article/Article";
import TopPanel from "./components/TopPanel/TopPanel";
import MapContainer from "./components/MapContainer/MapContainer";
import RegionNameWithButtons from "./components/RegionNameWithButtons/RegionNameWithButtons";
import NoArticlesText from "./components/NoArticlesText/NoArticlesText";

function App() {
  const [totalArticles, setTotalArticles] = useState(region_data);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [articles, setArticles] = useState([]);
  const [requestOffset, setRequestOffset] = useState(0);
  const [timeConfig, setTimeConfig] = useState({fromTime: DEFAULT_START_TIMESTAMP,
                                                            toTime: DEFAULT_END_TIMESTAMP});

    return (
        <div className="App">
            <div className="MainPanel">
                <TopPanel
                    timeConfig={timeConfig}
                    totalArticles={totalArticles}
                    setTimeConfig={setTimeConfig}
                    setArticles={setArticles}
                    setSelectedRegion={setSelectedRegion}
                    setTotalArticles={setTotalArticles}
                />
                <MapContainer
                    totalArticles={totalArticles}
                    setSelectedRegion={setSelectedRegion}
                    setArticles={setArticles}
                    timeConfig={timeConfig}
                    setRequestOffset={setRequestOffset}
                />
                <div className="EmptyPanel"></div>
            </div>
            <div className="SidePanel">
                <RegionNameWithButtons
                    setArticles={setArticles}
                    setRequestOffset={setRequestOffset}
                    requestOffset={requestOffset}
                    selectedRegion={selectedRegion}
                    timeConfig={timeConfig}
                    totalArticlesInRegion={selectedRegion ? totalArticles[selectedRegion - 1].numArticles : null}
                />
                <div className="Articles">
                    {articles.length === 0
                        ? <NoArticlesText/>
                        : articles.map((article, index) =>
                            <div style={{display: "flex", justifyContent: "center"}}><Article key={article.article_id} number={index + 1} article={article}/></div>
                        )
                    }
                </div>
            </div>
        </div>
    );
}

export default App;
