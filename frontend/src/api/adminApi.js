import instance from "./init";

export default {
    login: async (data) => {
        const response = await instance.post('/api/admin/login', data);
        return response.data
    }
}