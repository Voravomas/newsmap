import React from 'react';
import Map from "./Map";
import cl from "./MapContainer.module.css"

const MapContainer = ({totalArticles, setSelectedRegion, setArticles, timeConfig, setRequestOffset}) => {
    return (
        <div className={cl.MapContainer}>
            <Map
                totalArticles={totalArticles}
                setSelectedRegion={setSelectedRegion}
                setArticles={setArticles}
                timeConfig={timeConfig}
                setRequestOffset={setRequestOffset}
            />
        </div>
    );
};

export default MapContainer;