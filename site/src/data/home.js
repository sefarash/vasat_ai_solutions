// Copy for the home page lists. Wording that states a fact about the business comes from the
// live site the owner already published; prices and names are joined in from data/site.json.

export const nav = [
  { href: "/#services", label: "Services" },
  { href: "/#industries", label: "Industries" },
  { href: "/#how-it-works", label: "How It Works" },
  { href: "/#why-us", label: "Why Vasat AI" },
  { href: "/#faq", label: "FAQ" },
  { href: "/#contact", label: "Contact" },
];

export const industryCopy = {
  hvac: { icon: "material-symbols:ac-unit", text: "Beat the Houston summer rush with instant call answering and AC repair booking." },
  "appliance-repair": { icon: "material-symbols:build-outline", text: "Book refrigerator and laundry repair jobs straight into your technician's calendar." },
  cleaning: { icon: "material-symbols:cleaning-services-outline", text: "Automated quote follow-ups and recurring booking reminders for cleaning crews." },
  plumbing: { icon: "material-symbols:plumbing", text: "Emergency leak and water heater calls answered around the clock, without missing one." },
  "electrical-roofing": { icon: "material-symbols:electric-bolt-outline", text: "Panel upgrade and roof inspection leads qualified and booked before they call someone else." },
};

export const serviceCopy = {
  "local-service-website": {
    icon: "material-symbols:language",
    tag: "Local SEO",
    tone: "blue",
    tagline: "A website that actually brings in jobs.",
    bullets: ["Mobile-optimized, fast-loading design", "Local SEO targeting for your service area", "Click-to-call and online booking built in", "Review showcase to build instant trust"],
  },
  "meta-ads": {
    icon: "material-symbols:campaign-outline",
    tag: "Social Scale",
    tone: "gold",
    tagline: "Facebook and Instagram campaigns that reach homeowners in your service area.",
    bullets: ["Meta Advantage+ AI targeting finds buyers automatically", "AI-generated ad creatives, copy, and variations", "Monthly performance reports with full transparency"],
  },
  "custom-crm": {
    icon: "material-symbols:hub-outline",
    tag: "Zero Busywork",
    tone: "blue",
    tagline: "Every lead tracked. Every follow-up automated.",
    bullets: ["Centralized lead dashboard", "Job pipeline: New → Booked → Completed → Invoiced", "Automated text + email follow-up sequences", "Customer history and repeat booking triggers"],
  },
};

export const voiceAgent = {
  tagline:
    "Never miss another call — day or night. Our voice AI answers inbound calls 24/7, qualifies the lead by service type, issue and location, and books the appointment straight into your calendar.",
  points: [
    { title: "24/7 Answering", text: "Nights, weekends & holidays covered" },
    { title: "Calendar Sync", text: "Google Calendar, Jobber, ServiceTitan & Housecall Pro" },
    { title: "Missed-Call Text", text: "Follow-up text within 5 minutes" },
  ],
};

export const steps = [
  {
    title: "We Scope Your Solution",
    text: "We start with a free strategy call to understand your business — your lead sources, current costs, and biggest gaps. We recommend exactly which services will move the needle for you, whether that's one or all four.",
    chip: "Free strategy call",
    icon: "material-symbols:monitoring",
  },
  {
    title: "We Build & Integrate Everything",
    text: "Our team builds your AI voice agent, CRM, website, and ad campaigns — all configured to your business, your market, and your calendar. You don't touch a single technical setting.",
    chip: "No technical setup on your end",
    icon: "material-symbols:rocket-launch-outline",
  },
  {
    title: "You Go Live & We Manage It",
    text: "Your system goes live within 5–7 business days. Leads come in, AI answers, CRM tracks, and ads run — all managed for you. You just show up and do the work.",
    chip: "Live within 5–7 business days",
    icon: "material-symbols:event-available-outline",
  },
];

export const reasons = [
  { icon: "material-symbols:ring-volume-outline", tone: "gold", title: "Never Miss Another Call", text: "Our AI answers every call — day, night, weekends and holidays — and texts back missed callers within 5 minutes." },
  { icon: "material-symbols:savings-outline", tone: "blue", title: "Built for Small Business", text: "Predictable monthly pricing. Start with one service and add more when you're ready. No bloated enterprise retainers." },
  { icon: "material-symbols:groups-outline", tone: "gold", title: "One Dedicated Team", text: "No finger-pointing between your web designer, ad buyer, and software tools. We own your entire growth stack under one roof." },
  { icon: "material-symbols:support-agent", tone: "blue", title: "Fully Managed for You", text: "We build it, integrate it and run it. You don't touch a single technical setting — you just show up and do the work." },
];

export const math = {
  text: "Shops that rely on Google LSA and a dispatcher typically spend $4,200–4,800 every month just to keep the phone ringing. The full stack system replaces that cycle for a fraction of the cost.",
  stats: [
    { value: "70%", label: "Average reduction in cost per lead", tone: "cobalt" },
    { value: "5–7 Days", label: "Typical time to go live", tone: "gold" },
    { value: "60s", label: "Average response to new leads", tone: "cobalt" },
  ],
};

export const testimonials = [
  {
    quote:
      "I was skeptical at first — I didn't think a robot could represent my HVAC business. But the AI sounds so natural that customers can't tell the difference. Within the first 30 days we booked 14 extra jobs we would have missed. It's paid for itself ten times over.",
    name: "Marcus R.",
    role: "Owner, Premier HVAC Services — Houston, TX",
  },
];
export const reservedSpots = 2;

export const faqs = [
  { q: "Do I have to buy the full package or can I start with just one service?", a: "You can start with any single service — many clients begin with just the AI Voice Agent or a new website and add more over time. There's no requirement to take the full stack. We'll recommend the right starting point on your strategy call." },
  { q: "Will my customers know they're talking to an AI?", a: "Our AI agents are designed to sound natural and professional. Most customers simply experience a fast, friendly response. The agent focuses on booking the job — not revealing what it is. That said, if a customer directly asks, the agent will be transparent." },
  { q: "How long does it take to get set up?", a: "Most clients are live within 5–7 business days. We handle the entire setup — building your agent, configuring your CRM, launching your website and ads — and test everything before going live." },
  { q: "Does it work with my current scheduling software?", a: "Yes. We integrate with Google Calendar, Jobber, ServiceTitan, Housecall Pro, and more. If you use something else, we'll scope the integration during your onboarding call." },
  { q: "What kinds of contractors is this best suited for?", a: "Vasat AI is built for home service businesses — HVAC, plumbing, appliance repair, roofing, electrical, general contracting, and more. If your business depends on inbound leads and phone bookings, this system is built for you." },
  { q: "Do you only work with appliance repair companies?", a: "No — we work with all home service contractors. Appliance repair is one of our core markets in Houston, but the system works for any business that books jobs over the phone or from inbound leads." },
  { q: "What is the Full Stack system and why is it better than individual services?", a: "The Full Stack combines all four services — AI Voice Agent, CRM, Website, and Meta Ads — into one integrated growth system. Leads come in through ads, get answered by AI, are tracked in the CRM, and followed up automatically. Each piece makes the others more effective. Individual services are a great starting point — the full stack is where the biggest ROI lives." },
];

export const trades = ["HVAC & Air Conditioning", "Appliance Repair", "Residential or Commercial Cleaning", "Plumbing & Rooter", "Electrical Services", "Roofing & Storm Restoration", "Other Home Service"];
