import { Helmet } from 'react-helmet-async';
import BulkOrderForm from '../components/BulkOrderForm';

const BulkOrders = () => {
  return (
    <div className="bg-slate-50 min-h-screen">
      <Helmet>
        <title>Bulk Orders & Corporate Gifting | Soham Gift</title>
        <meta name="description" content="Contact us for bulk corporate gifting solutions. We offer tailored gifts and special pricing for Corporates, Event Planners, and Retail Stores." />
      </Helmet>
      

      
      <BulkOrderForm />
    </div>
  );
};

export default BulkOrders;
