import React from "react";


export const EmptyPage = () => {
    return (
        <div className="empty-page-container" style={{margin: '45px 0 0 53px'}}>
            <div className="empty-page-header">
                <h2>Oops :(</h2>
            </div>
            <div className="empty-page-text">
                Sorry, but we couldn't find anything matching your filters. Try to choose something else or contact a little later
            </div>
        </div>
    )
}