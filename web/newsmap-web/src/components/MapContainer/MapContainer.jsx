import React from 'react';
import Map from "./Map";
import cl from "./MapContainer.module.css"

const MapContainer = ({totalArticles, setSelectedRegion, setArticles, timeConfig, setRequestOffset}) => {
    return (
        <div className={cl.MapContainer}>
            <div className={cl.Map}>
                <Map
                    totalArticles={totalArticles}
                    setSelectedRegion={setSelectedRegion}
                    setArticles={setArticles}
                    timeConfig={timeConfig}
                    setRequestOffset={setRequestOffset}
                />
            </div>
        </div>
    );
};

export default MapContainer;