export const BACKEND_URL = process.env.REACT_BACKEND_URL || "http://localhost:8000";

const DEFAULT_OPTS: RequestInit = { credentials: "include" };

interface APICallProps<Type> {
  path: string;
  method?: string;
  options?: object
  onSuccess: (res: Response) => Type;
  onError?: (err: Error) => any;
}

export function make_api_call<Type>({
  path,
  method = "GET",
  options = {},
  onSuccess,
  onError = (err) => {},
}: APICallProps<Type>): Promise<Type> {
  const url = `${BACKEND_URL}${path}`;
  return fetch(url, { ...DEFAULT_OPTS, ...options, method: method })
    .then(onSuccess)
    .catch(onError);
}

export const callIsLoggedIn = () => {
  return make_api_call<boolean>({
    path: "/app/me",
    onSuccess: (res) => {
      return res.ok;
    },
    onError: (err) => {
      console.log(err);
    },
  });
};

export const callLogout = () => {
  return make_api_call<boolean>({
    path: "/auth/logout",
    method: "POST",
    onSuccess: (res) => {
      return res.ok;
    },
    onError: (err) => {
      console.log(err);
      throw err;
    },
  });
};
