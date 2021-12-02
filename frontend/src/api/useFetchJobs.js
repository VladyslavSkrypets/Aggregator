import { useReducer, useEffect } from "react";
import { jobsApi } from ".";

const ACTIONS = {
    MAKE_REQUEST: 'make-request',
    GET_DATA: 'get-data',
    ERROR: 'error',
    UPDATE_HAS_NEXT_PAGE: 'update-has-next-page'
}


function jobsReducer(state, action) {
    switch (action.type) {
        case ACTIONS.MAKE_REQUEST:
            return {loading: true, jobs: []}

        case ACTIONS.GET_DATA:
            return {...state, loading: false, jobs: action.payload.jobs}

        case ACTIONS.ERROR:
            return {...state, loading: false, error: action.payload.error, jobs: []}

        case ACTIONS.UPDATE_HAS_NEXT_PAGE:
            return {...state, hasNextPage: action.payload.hasNextPage}

        default:
            return state
    }
}

function jobReducer(state, action) {

}


export default function useFetchJobs(page, uid) {
    const [state, dispatch] = useReducer(jobsReducer, {jobs: [], loading: true})

    useEffect(async () => {
        dispatch({type: ACTIONS.MAKE_REQUEST})
        const jobsRequest = await jobsApi.getJobs(page);
        dispatch({type: ACTIONS.GET_DATA, payload: {jobs: jobsRequest['jobs']}})
        dispatch({type: ACTIONS.UPDATE_HAS_NEXT_PAGE, payload: {hasNextPage: jobsRequest['next_page']}})
        // const nextPageRequest = await jobsApi.getJobs(page + 1);
        // dispatch({type: ACTIONS.UPDATE_HAS_NEXT_PAGE, payload: {hasNextPage: nextPageRequest['jobs'].length !== 0}})
    }, [page])

    return state

}

export default function useFetchJob(uid) {
    const [state, dispatch] = useReducer(jobsReducer, {jobs: [], loading: true})

}