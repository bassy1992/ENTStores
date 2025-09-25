import { Card, CardContent } from '../ui/card';

export default function TestReview() {
  return (
    <Card>
      <CardContent className="p-8">
        <h2 className="text-xl font-bold mb-4">Test Review Component</h2>
        <p>This is a simple test to see if review components can render.</p>
        <div className="mt-4 p-4 bg-blue-50 rounded">
          <p className="text-blue-800">If you can see this, the component system is working!</p>
        </div>
      </CardContent>
    </Card>
  );
}