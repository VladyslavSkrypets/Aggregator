import { useReducer, useEffect } from "react";
import { adminApi } from ".";

const ACTIONS = {
    MAKE_REQUEST: 'make-request',
    GET_DATA: 'get-data',
    ERROR: 'error',
}

function reducer(state, action) {
    switch (action.type) {
        case ACTIONS.MAKE_REQUEST:
            return {loading: true, adminInfo: {}}

        case ACTIONS.GET_DATA:
            return {...state, loading: false, adminInfo: action.payload.adminInfo}

        case ACTIONS.ERROR:
            return {...state, loading: false, error: action.payload.error, adminInfo: {}}

        default:
            return state
    }
}

export function useFetchAdminInfo() {
    const [state, dispatch] = useReducer(reducer, {adminInfo: {}, loading: true})

    useEffect(async () => {
        dispatch({type: ACTIONS.MAKE_REQUEST});
        const response = await adminApi.getAdminInfo();
        dispatch({type: ACTIONS.GET_DATA, payload: {adminInfo: response['info']}})
    }, [])

    return state

}