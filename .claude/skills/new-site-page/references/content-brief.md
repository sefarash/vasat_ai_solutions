# Content brief by page type

The reader is the owner of a small home-service company (HVAC, appliance repair, plumbing, cleaning, electrical), usually on a phone between jobs. They want to know three things fast: is this for a business like mine, what do I get, what does it cost. Write plainly, in second person, and lead with the outcome (answered calls, booked jobs) rather than the technology.

## Service page (`/services/<slug>`), about 600+ words

1. H1 from the plan, then two sentences: the problem and what this service does about it.
2. What is included, as a short list of concrete deliverables.
3. How it works, in three or four steps, with how long setup takes if the owner has confirmed a number.
4. Price, read from `data/site.json` (monthly and setup). State what is not included.
5. Who it suits and who it does not.
6. Three to five FAQs that a contractor really asks (contract length, what happens to calls after hours, who owns the website or the ad account). These also feed the page's FAQ schema.
7. One call to action: the booking link from `data/site.json`.

## Industry page (`/industries/<slug>`), about 500+ words

1. H1 from the plan, then the specific pain of that trade (seasonal call spikes for HVAC, emergency calls for plumbing).
2. Which services matter most for this trade and why, linking to each service page.
3. A real example from that trade if the owner has one with permission. If not, leave the section out; do not write a composite.
4. Two or three trade-specific FAQs.
5. The booking call to action.

It must not be another industry page with the trade name swapped. If there is nothing specific to say about a trade yet, the page is not ready to be written.

## Landing page (`/lp/<slug>`), short

One promise that matches the ad, one form or booking button, proof if real proof exists, no navigation out. Claims and prices must match the service page exactly. Always noindex.

## Every page

- Title ≤ 60 characters, meta 70–155, both from the plan.
- No statistic, customer name, quote or integration that the owner has not confirmed.
- Avoid absolutes ("never miss a call", "guaranteed", "0 risk") unless there is a written guarantee behind them.
- Images need real alt text.
