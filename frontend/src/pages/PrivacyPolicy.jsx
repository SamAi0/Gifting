import { Helmet } from 'react-helmet-async';

const PrivacyPolicy = () => {
  return (
    <div className="pt-32 pb-20 bg-slate-50 min-h-screen">
      <Helmet>
        <title>Privacy Policy | Soham Gift</title>
        <meta name="description" content="Privacy Policy for Soham Gift. Learn how we handle your data securely." />
      </Helmet>
      
      <div className="container-custom max-w-4xl">
        <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-slate-100">
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-2">Privacy Policy</h1>
          <p className="text-slate-500 mb-8">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>
          
          <div className="prose prose-slate max-w-none prose-headings:text-slate-900 prose-p:text-slate-600 prose-li:text-slate-600">
            <h2 className="text-xl font-bold mt-8 mb-4">1. Introduction</h2>
            <p className="mb-4">
              Welcome to Soham Gift. We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you as to how we look after your personal data when you visit our website and tell you about your privacy rights and how the law protects you.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">2. The Data We Collect About You</h2>
            <p className="mb-4">
              We may collect, use, store and transfer different kinds of personal data about you which we have grouped together as follows:
            </p>
            <ul className="list-disc pl-6 mb-4 space-y-2">
              <li><strong>Identity Data</strong> includes first name, last name, username or similar identifier.</li>
              <li><strong>Contact Data</strong> includes billing address, delivery address, email address and telephone numbers.</li>
              <li><strong>Transaction Data</strong> includes details about payments to and from you and other details of products and services you have purchased from us.</li>
              <li><strong>Technical Data</strong> includes internet protocol (IP) address, your login data, browser type and version, time zone setting and location, and other technology on the devices you use to access this website.</li>
            </ul>

            <h2 className="text-xl font-bold mt-8 mb-4">3. How We Use Your Personal Data</h2>
            <p className="mb-4">
              We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:
            </p>
            <ul className="list-disc pl-6 mb-4 space-y-2">
              <li>Where we need to perform the contract we are about to enter into or have entered into with you (e.g., fulfilling your order).</li>
              <li>Where it is necessary for our legitimate interests (or those of a third party) and your interests and fundamental rights do not override those interests.</li>
              <li>Where we need to comply with a legal obligation.</li>
            </ul>

            <h2 className="text-xl font-bold mt-8 mb-4">4. Disclosures of Your Personal Data</h2>
            <p className="mb-4">
              We may share your personal data with the parties set out below for the purposes set out in section 3 above:
            </p>
            <ul className="list-disc pl-6 mb-4 space-y-2">
              <li>Service providers acting as processors who provide IT and system administration services.</li>
              <li>Third parties such as payment gateways (e.g., Razorpay) and delivery partners required to process and fulfill your orders.</li>
              <li>Professional advisers acting as processors or joint controllers including lawyers, bankers, auditors and insurers.</li>
            </ul>

            <h2 className="text-xl font-bold mt-8 mb-4">5. Data Security</h2>
            <p className="mb-4">
              We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed. In addition, we limit access to your personal data to those employees, agents, contractors and other third parties who have a business need to know.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">6. Your Legal Rights</h2>
            <p className="mb-4">
              Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to request access, correction, erasure, restriction, transfer, or to object to processing.
            </p>

            <h2 className="text-xl font-bold mt-8 mb-4">7. Contact Us</h2>
            <p className="mb-4">
              If you have any questions about this privacy policy or our privacy practices, please contact us at our provided contact details.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
