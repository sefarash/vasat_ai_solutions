// The only doorway to business facts and the page plan. Components import from here,
// never from a literal: see .claude/skills/project-conventions.
import site from "../../../data/site.json";
import plan from "../../../data/pages.json";

export { site };
export const business = site.business;
export const booking = site.booking;
export const leadForm = site.lead_form;
export const services = site.services;
export const plans = site.plans;
export const industries = site.industries;

export const service = (slug) => services.find((s) => s.slug === slug);
export const usd = (n) => "$" + Number(n).toLocaleString("en-US");

/** Title, meta, H1 and index flag for a route, from data/pages.json. */
export function page(route) {
  const entry = plan.pages.find((p) => p.route === route);
  if (!entry) throw new Error(`${route} is not in data/pages.json. Add it with tools/page_plan.py add.`);
  return entry;
}
export const plannedPages = plan.pages;
