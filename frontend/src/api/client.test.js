import { api } from "./client";

describe("api.hangars", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("list calls GET /api/hangars/ and returns json", async () => {
    const data = [{ id: "H-01", name: "Main", location: "Madrid" }];
    fetch.mockResolvedValueOnce({ ok: true, json: async () => data });

    const result = await api.hangars.list();

    expect(fetch).toHaveBeenCalledWith("/api/hangars/", {
      method: "GET",
      headers: {},
      body: undefined,
    });
    expect(result).toEqual(data);
  });

  it("list throws on non-ok response", async () => {
    fetch.mockResolvedValueOnce({ ok: false, status: 500, statusText: "Internal Server Error" });

    await expect(api.hangars.list()).rejects.toThrow("500 Internal Server Error");
  });

  it("create calls POST /api/hangars/ with JSON body", async () => {
    const payload = { id: "H-02", name: "West", location: "Barajas" };
    fetch.mockResolvedValueOnce({ ok: true, json: async () => payload });

    await api.hangars.create(payload);

    expect(fetch).toHaveBeenCalledWith("/api/hangars/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  });
});

describe("api entity shortcuts", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    fetch.mockResolvedValue({ ok: true, json: async () => [] });
  });

  afterEach(() => { vi.unstubAllGlobals(); });

  it("airplanes.list calls /api/airplanes/", async () => {
    await api.airplanes.list();
    expect(fetch).toHaveBeenCalledWith("/api/airplanes/", expect.any(Object));
  });

  it("flights.list calls /api/flights/", async () => {
    await api.flights.list();
    expect(fetch).toHaveBeenCalledWith("/api/flights/", expect.any(Object));
  });

  it("passengers.list calls /api/passengers/", async () => {
    await api.passengers.list();
    expect(fetch).toHaveBeenCalledWith("/api/passengers/", expect.any(Object));
  });
});
