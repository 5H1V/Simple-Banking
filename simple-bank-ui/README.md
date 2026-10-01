# Simple Bank UI

React and Vite frontend for Simple Bank.

## Run locally

```sh
npm install
npm run dev
```

The welcome page is available at `/`. User management is at `/users`. Visit `/accounts` to create an account for an existing user or look up account details by account ID. To deposit or withdraw from an existing account, visit `/transactions` and enter its account ID and a positive amount (up to two decimal places). The API must be running at `http://127.0.0.1:5000`. Direct visits to these routes work in the Vite dev server; production hosts must serve `index.html` for client-side routes.

Run `npm run build` to build for production and `npm run lint` to check the source.
